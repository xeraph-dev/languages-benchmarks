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

    let (zeroes, cmp) = match std::env::args().nth(2) {
        Some(v) => match v.parse::<usize>() {
            Ok(v) => match v & 1 {
                1 => (Arc::from((v + 1) / 2), Arc::<u8>::from(0x0F)),
                0 => (Arc::from(v / 2), Arc::<u8>::from(0x00)),
                _ => panic!("bad `is_odd` operation"),
            },
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
    // if result.as_ref == 2 {}

    // for _ in 0.. {
    let mut children = Vec::new();
    for i in 0..default_parallelism_approx {
        let share_cmp = cmp.clone();
        let len: Arc<usize> = zeroes.clone();
        let share_key = key.clone();
        let share_result = Arc::clone(&result);
        let child = thread::spawn(move || {
            iterate(
                i as isize,
                default_parallelism_approx,
                share_result,
                share_key,
                share_cmp,
                len,
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
    cmp: Arc<u8>,
    len: Arc<usize>,
) {
    let initial: &str = &key;
    for i in (start..).step_by(step) {
        // TODO condition to exit
        let r = result.load(Relaxed);
        if r >= 0 && r < i {
            return;
        }

        let mut input = String::from(initial);
        input = input.add(&i.to_string());

        let digest = md5::compute(input.as_bytes());

        let sliced: &[u8] = &digest.as_slice()[0..*(len.as_ref())];

        if sliced[sliced.len() - 1] > *(cmp.as_ref()) {
            continue;
        }

        let mut is_zeroed = true;
        for j in (0..sliced.len() - 1).rev() {
            if sliced[j] != 0 {
                is_zeroed = false;
                break;
            }
        }

        if is_zeroed {
            let r = result.load(Relaxed);
            if r == -1 || r > i {
                result.store(i, Relaxed)
            }
            return;
        }
    }
}
