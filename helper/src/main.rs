extern crate http;
extern crate redis;
extern crate serde;

use http::Request;

use redis::{Client, Commands};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::mpsc;
use std::thread::JoinHandle;
use std::{env, thread};

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

struct Describo {
    session_id: String,
    token: String,
}

#[derive(Clone, Debug)]
struct Config {
    client: Client,
    describo: String,
}
fn main() {
    println!("Starting up token synchronization between TokenStorage and Describo Online.");

    let redis_host = match env::var("REDIS_HOST") {
        Ok(val) => val,
        Err(_) => "localhost".to_string(),
    };
    let redis_port = match env::var("REDIS_PORT") {
        Ok(val) => val,
        Err(_) => "6379".to_string(),
    };

    let client = Client::open(format!("redis://{}:{}", redis_host, redis_port)).unwrap();
    let _url = match env::var("RDS_INSTALLATION_DOMAIN") {
        Ok(v) => format!("{}/port-service", v).to_string(),
        Err(_) => {
            eprintln!("Error: Envvar 'RDS_INSTALLATION_DOMAIN' not present. Trying 'USE_CASE_SERVICE_PORT_SERVICE'.");
            match env::var("USE_CASE_SERVICE_PORT_SERVICE") {
                Ok(v) => v,
                Err(_) => {
                    eprintln!("Error: Envvar 'USE_CASE_SERVICE_PORT_SERVICE' not present, too.");
                    return;
                }
            }
        }
    };
    let describo = match env::var("DESCRIBO_API_ENDPOINT") {
        Ok(v) => v,
        Err(_) => {
            eprintln!("Error: Envvar 'DESCRIBO_API_ENDPOINT' not present.");
            return;
        }
    };

    let config = Config { client, describo };

    start(config).unwrap();
}

fn start_redis_listener(
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
            let msg = pubsub.get_message().unwrap();
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

fn start_lookup_userid_in_redis(
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

fn start_update_describo(config: Config, describo_rcv: mpsc::Receiver<Describo>) -> JoinHandle<()> {
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

fn start(config: Config) -> Result<(), String> {
    // make request put method to describo to update access_token for sid
    let (redis, h1) =
        start_redis_listener(config.clone(), "TokenStorage_Refresh_Token".to_string());
    let (describo, h2) = start_lookup_userid_in_redis(config.clone(), redis);
    let h3 = start_update_describo(config.clone(), describo);

    h1.join().unwrap();
    h2.join().unwrap();
    h3.join().unwrap();

    Ok(())
}
