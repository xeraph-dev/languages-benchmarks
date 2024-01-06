import Foundation

let position = Int(CommandLine.arguments[1])!
var numbers = CommandLine.arguments[2...].map { Int($0)! }

struct NumberSpoken {
    var last: Int
    var prev: Int?

    mutating func move(_ turn: Int) {
        prev = last
        last = turn
    }
}

var spoken = numbers.last!
var spokens: [NumberSpoken?] = Array(repeating: nil, count: position)

extension [NumberSpoken?] {
    mutating func speak(_ turn: Int, _ val: Int) {
        if self[val] == nil {
            self[val] = .init(last: turn)
        } else {
            self[val]!.move(turn)
        }
        spoken = val
    }
}

for (idx, num) in numbers.enumerated() {
    spokens[num] = .init(last: idx + 1, prev: nil)
}

for turn in numbers.count + 1 ... position {
    if let num = spokens[spoken], let prev = num.prev {
        spokens.speak(turn, num.last - prev)
    } else {
        spokens.speak(turn, 0)
    }
}

print(spoken)
