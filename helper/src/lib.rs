extern crate redis;
extern crate serde;

use http::Request;
use redis::{Client, Commands};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
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

pub struct Describo {
    session_id: String,
    token: String,
}

#[derive(Clone, Debug)]
pub struct Config {
    pub client: Client,
    pub describo: String,
}

pub fn start_redis_listener(
    config: Config,
    channel: String,
) -> (mpsc::Receiver<String>, JoinHandle<()>) {
    let (sender, receiver) = mpsc::sync_channel(1000);

    let handle = thread::spawn(move || {
        let mut con = match config.client.get_connection() {
            Ok(v) => v,
            Err(_) => {
                panic!("Redis not available");
            }
        };

        // subscribe redis key "TokenStorage_Refresh_Token", wait for data
        let mut pubsub = con.as_pubsub();
        pubsub.subscribe(channel).unwrap();

        println!("Start redis listener");

        loop {
            println!("Wait for message.");
            let msg = match pubsub.get_message() {
                Ok(v) => v,
                Err(_) => {
                    panic!("Lost connection to redis.");
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
                println!("There was an critical error while sending payload.");
                break;
            }
        }
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
        let mut con = config.client.get_connection().unwrap();

        for payload in payloads_rcv {
            println!("got payload: {:?}", payload);
            let t: Token = serde_json::from_str(&payload).unwrap();

            // lookup in redis for user_id to get sessionId
            let session_id: String = match con.get(&(t.user.username)) {
                Ok(v) => v,
                Err(_) => {
                    println!("{} not found in redis.", t.user.username);
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
            let mut map = HashMap::new();
            map.insert("sessionId", d.session_id);
            map.insert("access_token", d.token);

            let res = Request::put(format!("{}/api/session/application", config.describo))
                .body(&map)
                .unwrap();
            println!("response from describo: {:?}", res)
        }
    });

    handle
}
