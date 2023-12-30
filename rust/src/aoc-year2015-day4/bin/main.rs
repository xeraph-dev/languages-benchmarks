use md5::{Digest, Md5};
use std::ops::Add;
use std::sync::atomic::AtomicIsize;
use std::sync::atomic::Ordering::Relaxed;
use std::sync::Arc;
use std::thread;
use std::thread::available_parallelism;

fn main() {
    let key: Arc<String> = match std::env::args().nth(1) {
        Some(v) => Arc::from(v),
        None => {
            println!("Key secret argument not found");
            std::process::exit(1)
        }
    };

    let zeroes = match std::env::args().nth(2) {
        Some(v) => match v.parse::<usize>() {
            Ok(v) => Arc::new(v),
            Err(err) => {
                eprintln!("Error parsing the zeroes {err}");
                std::process::exit(1)
            }
        },
        None => {
            eprintln!("Zeroes argument not found");
            std::process::exit(1)
        }
    };

    if *(zeroes.as_ref()) > 32 {
        eprintln!(
            "Number of zeroes cannot be greater than 32. (hex encode of md5 digest has 32 digits)"
        );
        std::process::exit(1)
    }

    let default_parallelism_approx = match available_parallelism() {
        Ok(v) => v.get(),
        Err(err) => {
            println!("Error getting paralelism {err}");
            std::process::exit(1)
        }
    };

    let result: Arc<AtomicIsize> = Arc::new(AtomicIsize::new(-1));

    let mut children = Vec::new();
    for i in 0..default_parallelism_approx {
        let share_zeroes = zeroes.clone();
        let share_key = key.clone();
        let share_result = Arc::clone(&result);
        let child = thread::spawn(move || {
            iterate(
                i as isize,
                default_parallelism_approx,
                share_result,
                share_key,
                share_zeroes,
            )
        });
        children.push(child)
    }

    for child in children {
        child.join().unwrap();
    }

    println!("{0}", result.load(Relaxed));
}

fn iterate(
    start: isize,
    step: usize,
    result: Arc<AtomicIsize>,
    key: Arc<String>,
    zeroes: Arc<usize>,
) {
    let initial: &str = &key;
    let zeroes = *(zeroes.as_ref());
    let len = match zeroes & 1 {
        1 => (zeroes + 1) / 2,
        0 => zeroes / 2,
        _ => panic!("bad `is_odd` operation"),
    };
    for i in (start..).step_by(step) {
        let r = result.load(Relaxed);
        if r >= 0 && r < i {
            return;
        }

        let mut input = String::from(initial);
        input = input.add(&i.to_string());

        let mut hasher = Md5::new();
        hasher.update(input.as_bytes());

        let digest = hasher.finalize();

        let sliced: &[u8] = &digest.as_slice()[0..len];

        let mut count_zeroes = 0;
        for j in 0..len {
            match sliced[j] {
                0 => count_zeroes += 2,
                _ => {
                    if j != len - 1 {
                        break;
                    }
                    if sliced[j] <= 0x0F {
                        count_zeroes += 1;
                    }
                }
            }
        }
        if count_zeroes == zeroes {
            let r = result.load(Relaxed);
            if r == -1 || r > i {
                result.store(i, Relaxed)
            }
            return;
        }
    }
}
