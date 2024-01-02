local md5         = require 'md5'

local secret      = arg[1]
local zeros_count = tonumber(arg[2])
local bytes_count = math.ceil(zeros_count / 2)

local candidate   = nil

local hash        = md5.new()
hash:update(secret)

local function startinZeros(sum)
  local zeros = 0
  for i = 1, bytes_count, 1 do
    local byte = sum:byte(i)
    if byte == 0x00 then
      zeros = zeros + 2
    elseif byte <= 0x0F then
      zeros = zeros + 1
      break
    else
      break
    end
  end
  return zeros
end

for i = 0, 2 ^ 32, 1 do
  local hashtmp = hash:clone()
  hashtmp:update(tostring(i))
  local sum = hashtmp:finish()
  if startinZeros(sum) == zeros_count then
    candidate = i
    break
  end
end


print(candidate)
