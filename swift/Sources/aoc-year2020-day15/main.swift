import Foundation

let position = UInt(CommandLine.arguments[1])!
var numbers = CommandLine.arguments[2...].map { UInt($0)! }

struct NumberSpoken {
    var last: UInt
    var prev: UInt?

    mutating func move(_ turn: UInt) {
        prev = last
        last = turn
    }
}

var spoken = numbers.last!
var spokens = [UInt: NumberSpoken]()

extension [UInt: NumberSpoken] {
    mutating func speak(_ turn: UInt, _ val: UInt) {
        if self[val] == nil {
            self[val] = .init(last: turn)
        } else {
            self[val]!.move(turn)
        }
        spoken = val
    }
}

for (idx, num) in numbers.enumerated() {
    spokens[num] = NumberSpoken(last: UInt(idx + 1), prev: nil)
}

for turn in UInt(numbers.count + 1) ... position {
    if let num = spokens[spoken], let prev = num.prev {
        spokens.speak(turn, num.last - prev)
    } else {
        spokens.speak(turn, 0)
    }
}

print(spoken)
