extern crate redis;
extern crate serde;

use redis::{Client, Commands};
use serde::{Deserialize, Serialize};
use serde_json::json;
use std::sync::mpsc;
use std::thread::{self, JoinHandle};

#[derive(Serialize, Deserialize, Debug)]
struct User {
    username: String,
}

#[derive(Serialize, Deserialize, Debug)]
struct Service {
    servicename: String,
}

#[derive(Serialize, Deserialize, Debug)]
struct Token {
    service: Service,
    access_token: String,
    user: User,
}

#[derive(Serialize, Deserialize, Debug)]
struct JSONToken {
    r#type: String,
    data: Token,
}

pub struct Describo {
    session_id: String,
    token: String,
}

#[derive(Clone)]
pub struct Config {
    pub client: Client,
    pub redis_channel: String,
    pub describo_url: String,
    pub describo_secret: String,
}

pub fn start_redis_listener(config: Config) -> (mpsc::Receiver<String>, JoinHandle<()>) {
    let (sender, receiver) = mpsc::sync_channel(1000);

    let handle = thread::spawn(move || {
        let mut con = config.client.get_connection().expect("Redis not available");

        // subscribe redis key "TokenStorage_Refresh_Token", wait for data
        let mut pubsub = con.as_pubsub();
        pubsub.subscribe(config.redis_channel).unwrap();

        println!("Start redis listener");

        loop {
            println!("Wait for message.");
            let msg = match pubsub.get_message() {
                Ok(v) => v,
                Err(_) => {
                    print!("Lost connection to redis.");
                    break;
                }
            };

            let payload: String = match msg.get_payload() {
                Ok(v) => {
                    println!("got message, channel '{}': {}", msg.get_channel_name(), v);
                    v
                }
                Err(_) => {
                    println!("Got no valid message from pubsub redis.");
                    continue;
                }
            };

            if sender.send(payload).is_err() {
                print!("There was an critical error while sending payload.");
                break;
            }
        }
        println!(" Quit redis pubsub thread.")
    });
    (receiver, handle)
}

pub fn start_lookup_userid_in_redis(
    config: Config,
    payloads_rcv: mpsc::Receiver<String>,
) -> (mpsc::Receiver<Describo>, JoinHandle<()>) {
    let (sender, receiver) = mpsc::sync_channel(1000);

    println!("Start sessionid lookup");

    let handle = thread::spawn(move || {
        let mut con = config.client.get_connection().expect("Redis not available");

        for payload in payloads_rcv {
            println!("got payload: {:?}", payload);

            let t: Token = match serde_json::from_str::<JSONToken>(&payload) {
                Ok(v) => v.data,
                Err(e1) => match serde_json::from_str::<Token>(&payload) {
                    Ok(v) => v,
                    Err(e2) => {
                        eprintln!("Payload error: \n{}\n\n{}", e1, e2);
                        continue;
                    }
                },
            };

            if t.service.servicename != "port-owncloud" {
                println!("skip: It is not for owncloud");
                continue;
            }

            // lookup in redis for user_id to get sessionId
            let session_id: String = match con.get(&(t.user.username)) {
                Ok(v) => v,
                Err(err) => {
                    if err.is_connection_dropped() {
                        println!("Redis not available");
                        break;
                    }
                    println!("key '{}' not found in redis.", t.user.username);
                    continue;
                }
            };

            println!("found sessionId: {}", session_id);
            if sender
                .send(Describo {
                    session_id,
                    token: t.access_token,
                })
                .is_err()
            {
                println!("There was an critical error while sending sessionId.");
                break;
            }
        }

        println!("Redis pubsub channel not sending anymore. Quit lookup userid in redis thread.");
    });

    (receiver, handle)
}

pub fn start_update_describo(
    config: Config,
    describo_rcv: mpsc::Receiver<Describo>,
) -> JoinHandle<()> {
    println!("Start describo session updater");

    let handle = thread::spawn(move || {
        for d in describo_rcv {
            let request_body = json!({
               "session": {
                  "owncloud": {
                      "access_token": d.token
                  }
               }
            });

            let res = reqwest::blocking::Client::new()
                .put(format!(
                    "{}/api/session/application/{}",
                    config.describo_url, d.session_id
                ))
                .bearer_auth(&config.describo_secret)
                .header("Content-Type", "application/json")
                .json(&request_body)
                .send();

            match res {
                Ok(v) => {
                    println!("response from describo: {:?}", v);
                }
                Err(err) => {
                    println!(
                        "Invalid request to describo, status_code: {}",
                        err.status().unwrap()
                    );
                }
            }
        }

        println!("Redis lookup channel not sending anymore. Quit describo updater thread.");
    });

    handle
}
