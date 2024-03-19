#include <cstdlib>
#include <cstring>
#include <iostream>
#include <mutex>
#include <openssl/md5.h>
#include <thread>

using namespace std;

class Data {
public:
  int canBeCandidate(int c) {
    lock_guard<mutex> lock(mu);
    return can(c);
  }

  int getCandidate() {
    lock_guard<mutex> lock(mu);
    return candidate;
  }

  void setCandidate(int c) {
    lock_guard<mutex> lock(mu);
    if (can(c)) {
      candidate = c;
    }
  }

  mutex mu;

private:
  int candidate;

  bool can(int c) { return candidate == 0 || c < candidate; }
};

void compute(Data *data, int cores, int step, MD5_CTX *md5, int md5_len,
             int zeros) {
  unsigned char hash[MD5_DIGEST_LENGTH];
  for (int index{step};; index += cores) {
    if (!data->canBeCandidate(index)) {
      break;
    }

    int zeros_count{};

    MD5_CTX copy;
    memcpy(&copy, md5, md5_len);

    auto buffer = to_string(index);

    MD5_Update(&copy, buffer.c_str(), buffer.size());
    MD5_Final(hash, &copy);

    for (int i{}; i < MD5_DIGEST_LENGTH; i++) {
      if (hash[i] == 0x00) {
        zeros_count += 2;
        continue;
      } else if (hash[i] <= 0x0F) {
        zeros_count += 1;
      }
      break;
    }

    if (zeros_count >= zeros) {
      data->setCandidate(index);
      break;
    }
  }
}

int main(int, char *argv[]) {
  auto data = new Data;

  auto secret{argv[1]};
  auto secret_len{strlen(secret)};

  auto zeros{atoi(argv[2])};

  auto cores{static_cast<int>(thread::hardware_concurrency())};

  MD5_CTX md5;
  auto md5_len{static_cast<int>(sizeof(md5))};
  MD5_Init(&md5);
  MD5_Update(&md5, secret, secret_len);

  thread threads[cores];

  for (int step{}; step < cores; step++) {
    threads[step] = thread(compute, data, cores, step, &md5, md5_len, zeros);
  }

  for (int step{}; step < cores; step++) {
    threads[step].join();
  }

  cout << data->getCandidate() << '\n';
}
