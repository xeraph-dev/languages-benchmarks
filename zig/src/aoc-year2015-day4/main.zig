const std = @import("std");
const md5 = std.crypto.hash.Md5;

var candidate: ?usize = null;
var m = std.Thread.Mutex{};
var wg = std.Thread.WaitGroup{};

fn compute(hashfn: md5, salt: u32, zeros: usize, step: usize, cpuCount: usize) !void {
    var buf: [20]u8 = undefined;
    var output: [md5.digest_length]u8 = undefined;
    var i = step;
    while (i <= salt) : (i += cpuCount) {
        if (candidate) |val| if (val <= i) break;

        var tmphash = hashfn;
        const salty = try std.fmt.bufPrint(&buf, "{d}", .{i});
        tmphash.update(salty);
        tmphash.final(&output);

        if (computeStartsWithCmp(&output, zeros)) {
            m.lock();
            candidate = i;
            m.unlock();
        }
    }

    wg.finish();
}

fn collide(str: []const u8, comptime salt: u32, zeros: usize) !void {
    var hashfn = md5.init(.{});
    hashfn.update(str);

    const cpuCount = try std.Thread.getCpuCount();

    for (0..cpuCount) |step| {
        wg.start();
        var thread = try std.Thread.spawn(.{}, compute, .{ hashfn, salt, zeros, step, cpuCount });
        thread.detach();
    }

    wg.wait();
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
    return zero_count == zeroes;
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
    try std.io.getStdOut().writer().print("{d}", .{candidate.?});
}
