let () =
  if (Array.length Sys.argv) == 3 then ()
  else (Printf.printf "needs at least 2 elements\n"; exit 1)

let parse_string s = 
  try int_of_string s
  with Failure _ -> (Printf.printf "fatal: could not parse %s\n" s; exit 1)
  
let char_zero = Char.chr 0
let char_15 = Char.chr 15

let zeros = parse_string Sys.argv.(2)
let secret = Bytes.of_string Sys.argv.(1)
let solution = ref (Int.max_int)
let mut = Mutex.create()

let md5_hash b =
  Digest.bytes b

let can_solve (str: string) _  =
  let zeros_count = ref 0 in
  let rec calc str i =
    let char = (String.unsafe_get str i) in
    if char  = char_zero then 
    begin
      zeros_count.contents <- zeros_count.contents + 2; 
      calc str (i + 1)
    end
    else if char = char_15 then
    begin
      zeros_count.contents <- zeros_count.contents + 1;
      calc str (i + 1)
    end
    else
      ()
  in
  calc str 0;
  zeros_count.contents >= zeros

let update_solution i =
  Mutex.lock mut;
  solution.contents <- i;
  Mutex.unlock mut

let int_to_str_byte x =
  let digits = Bytes.create 20 in
  let rec convert x i =
    if x = 0 && i >= 0 then Bytes.sub digits (i + 1) (19 - i)
    else if i >= 0 then
      let currentDigit = Int.rem x 10 in
      let x = Int.div x 10 in
      Bytes.set digits i (Char.chr (currentDigit + 48));
      convert x (i - 1)
    else 
      Bytes.sub digits (i + 1) (19 - i)
  in
  convert x 19

let rec solve i step =
  if i < solution.contents then
    if (can_solve (md5_hash (Bytes.cat secret (int_to_str_byte i)))) i then
      update_solution i
    else
      solve (i + step) step
  else
    ()

let () =
    let domains = Domain.recommended_domain_count() in
    let arr = ref [] in
    for i = 0 to domains-1 do
      let d = Domain.spawn (fun _ -> solve i domains) in
      arr.contents <- List.append arr.contents [d]
    done;
    let f elem = 
      Domain.join elem
    in
      List.iter f  arr.contents;;
    Printf.printf "%i\n" solution.contents