// Copyright 2024 xeraph. All rights reserved.
// Use of this source code is governed by a BSD-style
// license that can be found in the LICENSE file.

#include <math.h>
#include <openssl/evp.h>
#include <pthread.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <sys/sysctl.h>

typedef struct {
  size_t cores;
  size_t core;
  size_t zeros;
  EVP_MD_CTX *ctx;
  size_t *found;
  pthread_rwlock_t *lock;
} data_t;

size_t ncpu(void);

EVP_MD_CTX *ctx_new(void);
void ctx_copy(EVP_MD_CTX *out, const EVP_MD_CTX *in);
void digest_init(EVP_MD_CTX *ctx, const EVP_MD *md);
void digest_update(EVP_MD_CTX *ctx, char *data, int data_len);
void digest_final(EVP_MD_CTX *ctx, unsigned char *hash, unsigned int *hash_len);

size_t hash_count_leading_zeros(unsigned char *hash, unsigned int hash_len);
size_t get_leading_zeros(const EVP_MD_CTX *ctx_global, size_t num);

void *run(void *arg);

int main(int argc, char **argv) {
  if (argc < 2) {
    fprintf(stderr, "missing secret\n");
    exit(EXIT_FAILURE);
  } else if (argc < 3) {
    fprintf(stderr, "missing zeros\n");
    exit(EXIT_FAILURE);
  }

  char *secret = argv[1];
  size_t secret_len = strlen(secret);

  size_t zeros = atol(argv[2]);

  size_t cores = ncpu();

  EVP_MD_CTX *ctx = ctx_new();
  const EVP_MD *md = EVP_md5();

  digest_init(ctx, md);
  digest_update(ctx, secret, secret_len);

  size_t found = 0;
  pthread_rwlock_t lock = PTHREAD_RWLOCK_INITIALIZER;

  pthread_t threads[cores];
  data_t threads_data[cores];

  for (size_t core = 0; core < cores; core++) {
    threads_data[core] = (data_t){
        .core = core + 1,
        .cores = cores,
        .zeros = zeros,
        .ctx = ctx,
        .found = &found,
        .lock = &lock,
    };
    pthread_create(&threads[core], NULL, run, &threads_data[core]);
  }

  for (size_t core = 0; core <= cores; core++) {
    pthread_join(threads[core], NULL);
  }

  printf("%zu\n", found);

  EVP_MD_CTX_free(ctx);
  return EXIT_SUCCESS;
}

void *run(void *arg) {
  data_t *data = arg;
  if (!data) {
    fprintf(stderr, "data cannot be NULL");
    pthread_exit(NULL);
  }

  for (size_t num = data->core; num < INT_MAX; num += data->cores) {
    pthread_rwlock_rdlock(data->lock);
    if (*data->found > 0 && num >= *data->found) {
      break;
    }
    pthread_rwlock_unlock(data->lock);

    if (data->zeros == get_leading_zeros(data->ctx, num)) {
      pthread_rwlock_wrlock(data->lock);
      *data->found = num;
      pthread_rwlock_unlock(data->lock);
      break;
    }
  }

  return NULL;
}

size_t get_leading_zeros(const EVP_MD_CTX *ctx_global, size_t num) {
  EVP_MD_CTX *ctx = EVP_MD_CTX_new();
  ctx_copy(ctx, ctx_global);

  unsigned char hash[EVP_MAX_MD_SIZE];
  unsigned int hash_len = 0;

  int buf_len = floor(log10(num)) + 1;
  char buf[buf_len];
  sprintf(buf, "%zu", num);

  digest_update(ctx, buf, buf_len);
  digest_final(ctx, hash, &hash_len);

  return hash_count_leading_zeros(hash, hash_len);
}

size_t hash_count_leading_zeros(unsigned char *hash, unsigned int hash_len) {
  size_t zeros_count = 0;

  for (size_t i = 0; i < hash_len; i++) {
    if (hash[i] == 0x00) {
      zeros_count += 2;
      continue;
    } else if (hash[i] <= 0x0F) {
      zeros_count += 1;
    }
    break;
  }

  return zeros_count;
}

EVP_MD_CTX *ctx_new(void) {
  EVP_MD_CTX *ctx = EVP_MD_CTX_new();
  if (ctx)
    return ctx;

  fprintf(stderr, "error creating new context\n");
  exit(EXIT_FAILURE);
}

void ctx_copy(EVP_MD_CTX *out, const EVP_MD_CTX *in) {
  if (EVP_MD_CTX_copy_ex(out, in))
    return;

  fprintf(stderr, "error copyting context\n");
  EVP_MD_CTX_free(out);
  exit(EXIT_FAILURE);
}

void digest_init(EVP_MD_CTX *ctx, const EVP_MD *md) {
  if (EVP_DigestInit_ex(ctx, md, NULL))
    return;

  fprintf(stderr, "error initializing digest\n");
  EVP_MD_CTX_free(ctx);
  exit(EXIT_FAILURE);
}

void digest_update(EVP_MD_CTX *ctx, char *data, int data_len) {
  if (EVP_DigestUpdate(ctx, data, data_len))
    return;

  fprintf(stderr, "error updating digest\n");
  EVP_MD_CTX_free(ctx);
  exit(EXIT_FAILURE);
}

void digest_final(EVP_MD_CTX *ctx, unsigned char *hash,
                  unsigned int *hash_len) {
  if (EVP_DigestFinal_ex(ctx, hash, hash_len))
    return;

  fprintf(stderr, "error finalizing digest\n");
  EVP_MD_CTX_free(ctx);
  exit(EXIT_FAILURE);
}

size_t ncpu(void) {
  int cores;
  size_t len = sizeof cores;

  if (sysctlbyname("hw.ncpu", &cores, &len, NULL, 0) == 0) {
    return cores;
  } else {
    perror("sysctlbyname");
  }

  exit(EXIT_FAILURE);
}
