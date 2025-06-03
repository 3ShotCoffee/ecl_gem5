/*
 * Copyright (c) 2022 The Regents of the University of California
 * All rights reserved
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met: redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer;
 * redistributions in binary form must reproduce the above copyright
 * notice, this list of conditions and the following disclaimer in the
 * documentation and/or other materials provided with the distribution;
 * neither the name of the copyright holders nor the names of its
 * contributors may be used to endorse or promote products derived from
 * this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

 #include <stdio.h>
 #include <stdlib.h>

 // Define min macro for integer values
 #ifndef min
 #define min(a,b) (((a)<(b))?(a):(b))
 #endif

 // Include the gem5 m5ops header file
 #include <gem5/m5ops.h>

 // Base case size — small enough to fit in L1
int base = 16;

// Cache-oblivious recursive matrix multiplication
void matmul_rec(int *A, int *B, int *C, int a_row, int a_col, int b_row, int b_col, int c_row, int c_col, int n, int N) {
    if (n <= base) {
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < n; ++j)
                for (int k = 0; k < n; ++k)
                    C[(c_row + i) * N + (c_col + j)] += A[(a_row + i) * N + (a_col + k)] * B[(b_row + k) * N + (b_col + j)];
    } else {
        int h = n / 2;
        // Divide into 8 recursive calls
        matmul_rec(A, B, C, a_row, a_col,     b_row, b_col,     c_row, c_col,     h, N);
        matmul_rec(A, B, C, a_row, a_col+h,   b_row+h, b_col,   c_row, c_col,     h, N);

        matmul_rec(A, B, C, a_row, a_col,     b_row, b_col+h,   c_row, c_col+h,   h, N);
        matmul_rec(A, B, C, a_row, a_col+h,   b_row+h, b_col+h, c_row, c_col+h,   h, N);

        matmul_rec(A, B, C, a_row+h, a_col,   b_row, b_col,     c_row+h, c_col,   h, N);
        matmul_rec(A, B, C, a_row+h, a_col+h, b_row+h, b_col,   c_row+h, c_col,   h, N);

        matmul_rec(A, B, C, a_row+h, a_col,   b_row, b_col+h,   c_row+h, c_col+h, h, N);
        matmul_rec(A, B, C, a_row+h, a_col+h, b_row+h, b_col+h, c_row+h, c_col+h, h, N);
    }
}

 int main(int argc, char *argv[])
 {
     if (argc < 2) {
         fprintf(stderr, "Usage: %s <MATSIZE> <BLOCKSIZE>\n", argv[0]);
         return 1;
     }

     const int size = atoi(argv[1]); // size (1D length) of matrices A, B and C
     base = atoi(argv[2]); // Block size for cache optimization
     int *A = malloc(size * size * sizeof(int));
     int *B = malloc(size * size * sizeof(int));
     int *C = malloc(size * size * sizeof(int));

     printf("[Cache-oblivious matrix multiplication]\n");
     printf("matrix size: %d x %d\n", size, size);
     printf("base case size: %d\n", base);

     printf("Populating matrices A and B...\n");
     for(int i = 0; i < size; i++)
     {
         for(int j = 0; j < size; j++)
         {
             A[i * size + j] = i + j;
             B[i * size + j] = (4 * i) + (7 * j);
         }
     }
     printf("Done!\n");

     printf("Thrashing the cache...\n");
     int *trash = malloc(10 * 1024 * 1024); // 10 MB
     for (int i = 0; i < (10 * 1024 * 1024) / sizeof(int); i++) {
         trash[i] = i;
     }
     free(trash);
     printf("Done!\n");

     printf("Multiplying the matrixes...\n");

     m5_reset_stats(0, 0); // Reset statistics here

     matmul_rec(A, B, C, 0, 0, 0, 0, 0, 0, size, size);

     m5_dump_stats(0, 0); // Dump statistics right after

     printf("Done!\n");

     printf("Calculating the sum of all elements in the matrix...\n");
     long int sum = 0;
     for(int x = 0; x < size; x++)
         for(int y = 0; y < size; y++)
             sum += C[x * size + y];
     printf("Done\n");

     printf("The sum is %ld\n", sum);

     free(A);
     free(B);
     free(C);
 }
