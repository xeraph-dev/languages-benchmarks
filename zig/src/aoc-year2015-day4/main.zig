const std = @import("std");
const md5 = std.crypto.hash.Md5;

fn collide(str: []const u8, comptime salt: u32, zeros: usize) !void {
    var output: [md5.digest_length]u8 = undefined;
    var buf: [20]u8 = undefined;
    var hashfn = md5.init(.{});
    hashfn.update(str);

    for (0..salt) |i| {
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
    var valid: bool = false;
    var byte_count: usize = 0;

    switch (zeroes) {
        5 => {
            for (str[0..3].*, 0..) |char, i| {
                if (char == 0x0 and i != 2) {
                    byte_count += 1;
                } else if ((char > 0x0 and char <= 0xF) and i == 2) {
                    byte_count += 1;
                } else return false;
            }
            if (byte_count == 3) valid = true;
        },
        6 => {
            for (str[0..3].*, 0..) |char, i| {
                _ = i;
                if (char == 0x0) {
                    byte_count += 1;
                } else return false;
            }
            if (byte_count == 3) valid = true;
        },
        7 => {
            for (str[0..4].*, 0..) |char, i| {
                if (char == 0x0 and i != 3) {
                    byte_count += 1;
                } else if ((char > 0x0 and char <= 0xF) and i == 3) {
                    byte_count += 1;
                } else return false;
            }
            if (byte_count == 4) valid = true;
        },
        else => unreachable,
    }
    return valid;
}

fn args() ![][:0]u8 {
    var sand = std.heap.ArenaAllocator.init(std.heap.raw_c_allocator);
    defer sand.deinit();
    var args_alloc = try std.process.argsAlloc(sand.allocator());
    if (args_alloc.len != 3) std.process.exit(1);
    return args_alloc[1..][0..];
}

fn parseArgZeroes(comptime T: type, buf: [:0]u8) !T {
    return std.fmt.parseInt(T, buf, 10) catch unreachable;
}

pub fn main() !void {
    const salt = std.math.maxInt(u32);
    var args_parsed = try args();
    const input = args_parsed[0];
    const number = try parseArgZeroes(usize, args_parsed[1]);
    try collide(input, salt, number);
}
