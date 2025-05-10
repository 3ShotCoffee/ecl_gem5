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

 // Include the gem5 m5ops header file
 #include <gem5/m5ops.h>

 int main(int argc, char *argv[])
 {
     if (argc < 3) {
         fprintf(stderr, "Usage: %s <MATSIZE> <BSIZE>\n", argv[0]);
         return 1;
     }

     const int size = atoi(argv[1]); // size (1D length) of matrices A, B and C
     const int block_size = atoi(argv[2]); // Block size for cache optimization
     int **A = malloc(size * sizeof(int *));
     int **B = malloc(size * sizeof(int *));
     int **C = malloc(size * sizeof(int *));

     for (int i = 0; i < size; i++) {
         A[i] = malloc(size * sizeof(int));
         B[i] = malloc(size * sizeof(int));
         C[i] = malloc(size * sizeof(int));
     }
     //int A[size][size], B[size][size], C[size][size];

     printf("[BLOCKED matrix multiplication]\n");
     printf("matrix size: %d x %d\n", size, size);
     printf("block size: %d\n", block_size);

     printf("Populating matrices A and B...\n");
     for(int i = 0; i < size; i++)
     {
         for(int j = 0; j < size; j++)
         {
             A[i][j] = i + j;
             B[i][j] = (4 * i) + (7 * j);
         }
     }
     printf("Done!\n");

     printf("Initializing matrix C...\n");
     for (int i = 0; i < size; i++)
     for (int j = 0; j < size; j++)
         C[i][j] = 0;
     printf("Done!\n");

     printf("Multiplying the matrixes...\n");

     m5_reset_stats(0, 0); // Reset statistics here

     /* blocked matrix multiplication with ijk */
     for (int jj = 0; jj < size; jj += block_size) {
         for (int kk = 0; kk < size; kk += block_size) {
             for (int i = 0; i < size; i++) {
                 for (int j = jj; j < jj + block_size && j < size; j++) {
                     int sum = 0;
                     for (int k = kk; k < kk + block_size && k < size; k++) {
                         sum += A[i][k] * B[k][j];
                     }
                     C[i][j] += sum;
                 }
             }
         }
     }

     m5_dump_stats(0, 0); // Dump statistics right after

     printf("Done!\n");

     printf("Calculating the sum of all elements in the matrix...\n");
     long int sum = 0;
     for(int x = 0; x < size; x++)
         for(int y = 0; y < size; y++)
             sum += C[x][y];
     printf("Done\n");

     printf("The sum is %ld\n", sum);

     for (int i = 0; i < size; i++) {
         free(A[i]);
         free(B[i]);
         free(C[i]);
     }
     free(A);
     free(B);
     free(C);

     return sum;
 }
