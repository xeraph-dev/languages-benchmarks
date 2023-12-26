import CryptoKit
import Foundation

let zeros = [UInt8](repeating: 0, count: 3)[...]

var hash = Insecure.MD5()
hash.update(data: [UInt8]("yzbqklnj".utf8))

for i in 0 ... UInt32.max {
    var hash = hash
    hash.update(data: [UInt8](i.description.utf8))
    if [UInt8](hash.finalize())[0 ... 2] == zeros {
        print(i)
        break
    }
}
