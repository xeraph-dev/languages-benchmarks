const std = @import("std");
const md5 = std.crypto.hash.Md5;

fn collide(str: []const u8, comptime salt: u32, zeros: usize) !void {
    var i: usize = 0;
    var output: [md5.digest_length]u8 = undefined;
    var buf: [20]u8 = undefined;
    var hashfn = md5.init(.{});
    hashfn.update(str);

    while (i < salt) : (i += 1) {
        var tmphash = hashfn;
        const salty = try std.fmt.bufPrint(&buf, "{d}", .{i});
        tmphash.update(salty);
        tmphash.final(&output);

        if (computeStartsWithCmp(&output, zeros)) {
            try std.io.getStdOut().writer().print("{any} - {d}\n", .{ std.fmt.fmtSliceHexLower(&output), i });
            break;
        }
    }
}

fn computeStartsWithCmp(str: []const u8, zeroes: usize) bool {
    if (zeroes == 0) return true;
    var zero_count: usize = 0;

    for (str) |char| {
        if (char == 0x0) {
            zero_count += 2;
            continue;
        }
        if (char <= 0xF) {
            zero_count += 1;
        }
        break;
    }
    if (zero_count == zeroes) return true;

    return false;
}

fn parseArgZeroes(comptime T: type, buf: [:0]const u8) !T {
    return std.fmt.parseInt(T, buf, 10) catch unreachable;
}

pub fn main() !void {
    var args = try std.process.argsWithAllocator(std.heap.raw_c_allocator);
    defer args.deinit();
    _ = args.skip();

    const salt = std.math.maxInt(u32);
    const input = args.next() orelse unreachable;
    const zeros = args.next() orelse unreachable;
    const number = try parseArgZeroes(usize, zeros);
    try collide(input, salt, number);
}
