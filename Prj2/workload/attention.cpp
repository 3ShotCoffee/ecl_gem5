#include <iostream>
#include <cmath>
#include <random>
#include <cstdlib>
#include <cstring>
#include <string>
#include <gem5/m5ops.h>

void randn(float* mat, int rows, int cols) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::normal_distribution<float> d(0.0f, 0.02f);
    for (int i = 0; i < rows * cols; ++i) {
        mat[i] = d(gen);
    }
}

inline float& at(float* mat, int row, int col, int cols) {
    return mat[row * cols + col];
}

void base_matmul(const float* A, const float* B, float* C, int M, int N, int K) {
    std::memset(C, 0, sizeof(float) * M * N);
    for (int i = 0; i < M; ++i)
        for (int k = 0; k < K; ++k)
            for (int j = 0; j < N; ++j)
                at(C, i, j, N) += at(const_cast<float*>(A), i, k, K) * at(const_cast<float*>(B), k, j, N);
}

void blocked_matmul(const float* A, const float* B, float* C,
                    int M, int N, int K, int blockSize) {
    std::memset(C, 0, sizeof(float) * M * N);
    for (int i0 = 0; i0 < M; i0 += blockSize) {
        for (int j0 = 0; j0 < N; j0 += blockSize) {
            for (int k0 = 0; k0 < K; k0 += blockSize) {
                for (int i = i0; i < std::min(i0 + blockSize, M); ++i) {
                    for (int k = k0; k < std::min(k0 + blockSize, K); ++k) {
                        float a_val = at(const_cast<float*>(A), i, k, K);
                        for (int j = j0; j < std::min(j0 + blockSize, N); ++j) {
                            at(C, i, j, N) += a_val * at(const_cast<float*>(B), k, j, N);
                        }
                    }
                }
            }
        }
    }
}

enum class Mode { BASE, BLOCKED };

int main(int argc, char* argv[]) {
    if (argc < 5) {
        std::cerr << "Usage: " << argv[0] << " <SEQ_LEN> <HIDDEN_DIM> <HEADS> <base|blocked> [block_size]\n";
        return 1;
    }

    int SEQ_LEN = std::atoi(argv[1]);
    int HIDDEN_DIM = std::atoi(argv[2]);
    int HEADS = std::atoi(argv[3]);
    Mode mode;
    int BLOCK_SIZE = 0;

    std::string mode_arg = argv[4];
    if (mode_arg == "base") {
        mode = Mode::BASE;
    } 
    else if (mode_arg == "blocked") {
        if (argc != 6) {
            std::cerr << "Error: Block size missing.\n";
            return 1;
        }
        BLOCK_SIZE = std::atoi(argv[5]);
        if (BLOCK_SIZE <= 0) {
            std::cerr << "Error: Block size must be positive.\n";
            return 1;
        }
        mode = Mode::BLOCKED;
    } 
    else {
        std::cerr << "Error: Unknown mode. Use 'base' or 'blocked'.\n";
        return 1;
    }

    if (HIDDEN_DIM % HEADS != 0) {
        std::cerr << "Error: HIDDEN_DIM must be divisible by HEADS\n";
        return 1;
    }

    int HEAD_DIM = HIDDEN_DIM / HEADS;

    // Input tensor: [SEQ_LEN x HIDDEN_DIM]
    float* x = new float[SEQ_LEN * HIDDEN_DIM];

    // Weights: [HIDDEN_DIM x HIDDEN_DIM] for Q, K, V and output
    float* W_q = new float[HIDDEN_DIM * HIDDEN_DIM];
    float* W_k = new float[HIDDEN_DIM * HIDDEN_DIM];
    float* W_v = new float[HIDDEN_DIM * HIDDEN_DIM];
    float* W_o = new float[HIDDEN_DIM * HIDDEN_DIM];

    float* Q = new float[SEQ_LEN * HIDDEN_DIM];
    float* K = new float[SEQ_LEN * HIDDEN_DIM];
    float* V = new float[SEQ_LEN * HIDDEN_DIM];
    float* concat = new float[SEQ_LEN * HIDDEN_DIM];
    float* output = new float[SEQ_LEN * HIDDEN_DIM];

    randn(x, SEQ_LEN, HIDDEN_DIM);
    randn(W_q, HIDDEN_DIM, HIDDEN_DIM);
    randn(W_k, HIDDEN_DIM, HIDDEN_DIM);
    randn(W_v, HIDDEN_DIM, HIDDEN_DIM);
    randn(W_o, HIDDEN_DIM, HIDDEN_DIM);

    m5_reset_stats(0, 0); // Reset statistics here

    // Choose the matrix multiplication function
    auto matmul = [&](const float* A, const float* B, float* C, int M, int N, int K) {
        if (mode == Mode::BASE)
            base_matmul(A, B, C, M, N, K);
        else
            blocked_matmul(A, B, C, M, N, K, BLOCK_SIZE);
    };

    // Compute Q, K, V
    matmul(x, W_q, Q, SEQ_LEN, HIDDEN_DIM, HIDDEN_DIM);
    matmul(x, W_k, K, SEQ_LEN, HIDDEN_DIM, HIDDEN_DIM);
    matmul(x, W_v, V, SEQ_LEN, HIDDEN_DIM, HIDDEN_DIM);

    // Multi-head attention
    for (int h = 0; h < HEADS; ++h) {
        int offset = h * HEAD_DIM;

        float* Qh = Q + offset;
        float* Kh = K + offset;
        float* Vh = V + offset;
        float* Ah = new float[SEQ_LEN * HEAD_DIM];
        float* score = new float[SEQ_LEN * SEQ_LEN];

        for (int i = 0; i < SEQ_LEN; ++i)
            for (int j = 0; j < SEQ_LEN; ++j) {
                float s = 0.0f;
                for (int d = 0; d < HEAD_DIM; ++d)
                    s += at(Qh, i, d, HEAD_DIM) * at(Kh, j, d, HEAD_DIM);
                at(score, i, j, SEQ_LEN) = s / std::sqrt((float)HEAD_DIM);
            }

        for (int i = 0; i < SEQ_LEN; ++i) {
            float sum = 0.0f;
            for (int j = 0; j < SEQ_LEN; ++j) {
                at(score, i, j, SEQ_LEN) = std::exp(at(score, i, j, SEQ_LEN));
                sum += at(score, i, j, SEQ_LEN);
            }
            for (int j = 0; j < SEQ_LEN; ++j)
                at(score, i, j, SEQ_LEN) /= sum;
        }

        // Compute attention score
        matmul(score, Vh, Ah, SEQ_LEN, HEAD_DIM, SEQ_LEN);

        for (int i = 0; i < SEQ_LEN; ++i)
            for (int d = 0; d < HEAD_DIM; ++d)
                at(concat, i, offset + d, HIDDEN_DIM) = at(Ah, i, d, HEAD_DIM);

        delete[] Ah;
        delete[] score;
    }

    matmul(concat, W_o, output, SEQ_LEN, HIDDEN_DIM, HIDDEN_DIM);

    m5_dump_stats(0, 0); // Dump statistics right after

    // Checksum to avoid dead-code elimination
    float sum = 0.0f;
    for (int i = 0; i < SEQ_LEN * HIDDEN_DIM; ++i)
        sum += output[i];

    std::cout << "Checksum: " << sum << "\n";

    // Cleanup
    delete[] x;
    delete[] W_q;
    delete[] W_k;
    delete[] W_v;
    delete[] W_o;
    delete[] Q;
    delete[] K;
    delete[] V;
    delete[] concat;
    delete[] output;

    return 0;
}
