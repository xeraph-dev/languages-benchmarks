use std::ops::Add;
use std::thread;
use std::thread::available_parallelism;

use byteorder::{BigEndian, ReadBytesExt};

const COMPARE: u32 = 255;

const INPUT: &str = "yzbqklnj";

fn main() {
    let default_parallelism_approx = available_parallelism().unwrap().get();

    let mut response = -1;
    let mut start = 0;
    for _ in 0.. {
        let mut children = Vec::new();
        for _ in 0..default_parallelism_approx {
            let child = thread::spawn(move || iterate(start, start + 1000));
            start += 1000;
            children.push(child);
        }

        for child in children {
            let r = child.join().unwrap();
            match r {
                Some(v) => {
                    if v < response || response == -1 {
                        response = v;
                    }
                }
                _ => {}
            }
        }
        if response != -1 {
            break;
        }
    }
    println!("{response}");
}

fn iterate(start: isize, end: isize) -> Option<isize> {
    let mut response: Option<isize> = None;
    for i in start..end {
        let mut input = String::from(INPUT);
        input = input.add(&i.to_string());

        let digest = md5::compute(input.as_bytes());

        let mut sliced: &[u8] = &digest.as_slice()[0..4];

        let num = sliced.read_u32::<BigEndian>().unwrap();

        if num | COMPARE == COMPARE {
            response = Some(i);
            break;
        }
    }
    response
}
