import CryptoKit
import Foundation

extension Digest {
    var startingZeros: UInt8 {
        var zeros: UInt8 = 0
        for byte in self {
            if byte == 0x00 {
                zeros += 2
                continue
            }
            if byte <= 0x0F {
                zeros += 1
            }
            break
        }
        return zeros
    }
}

var args = CommandLine.arguments
var secret = args[1]
var zeros = UInt8(args[2])!

var hash = Insecure.MD5()
hash.update(data: [UInt8](secret.utf8))

for i in 0 ... UInt32.max {
    var hash = hash
    hash.update(data: [UInt8](i.description.utf8))
    if hash.finalize().startingZeros == zeros {
        print(i)
        break
    }
}
