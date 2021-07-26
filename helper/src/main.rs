extern crate http;
extern crate redis;
extern crate serde;

use helper::Config;
use redis::Client;
use std::env;

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
                    panic!("Error: Envvar 'USE_CASE_SERVICE_PORT_SERVICE' not present, too.");
                }
            }
        }
    };
    let describo = match env::var("DESCRIBO_API_ENDPOINT") {
        Ok(v) => v,
        Err(_) => {
            panic!("Error: Envvar 'DESCRIBO_API_ENDPOINT' not present.");
        }
    };

    let config = helper::Config { client, describo };

    start(config).unwrap();
}

fn start(config: Config) -> Result<(), String> {
    // make request put method to describo to update access_token for sid
    let (redis, h1) =
        helper::start_redis_listener(config.clone(), "TokenStorage_Refresh_Token".to_string());
    let (describo, h2) = helper::start_lookup_userid_in_redis(config.clone(), redis);
    let h3 = helper::start_update_describo(config.clone(), describo);

    h1.join().unwrap();
    h2.join().unwrap();
    h3.join().unwrap();

    Ok(())
}
