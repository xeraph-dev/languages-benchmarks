let () =
  if (Array.length Sys.argv) == 3 then ()
  else (Printf.printf "needs at least 2 elements\n"; exit 1)

let parse_string s = 
  try int_of_string s
  with Failure _ -> (Printf.printf "fatal: could not parse %s\n" s; exit 1)
  
let zeros = parse_string Sys.argv.(2)
let secret = Sys.argv.(1)
let solution = ref (Int.max_int)
let mut = Mutex.create()

let md5_hash str =
  let digest = Digest.string str in
  Digest.to_hex digest

let rec can_solve str count idx =
    if String.get str idx == '0' then
      if count >= zeros then 
        true
      else 
        can_solve str (count + 1) (idx + 1)
    else
      false

let update_solution i =
  Mutex.lock mut;
  solution.contents <- i;
  Mutex.unlock mut

let rec solve i step =
  if i < solution.contents then
    if (can_solve (md5_hash (secret ^ string_of_int i)) 1 0) then
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