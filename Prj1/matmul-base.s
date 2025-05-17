	.file	"matmul-base.c"
	.text
	.section	.rodata
.LC0:
	.string	"Usage: %s <MATSIZE> \n"
.LC1:
	.string	"[BASE matrix multiplication]"
.LC2:
	.string	"matrix size: %d x %d\n"
	.align 8
.LC3:
	.string	"Populating matrices A and B..."
.LC4:
	.string	"Done!"
.LC5:
	.string	"Multiplying the matrixes..."
	.align 8
.LC6:
	.string	"Calculating the sum of all elements in the matrix..."
.LC7:
	.string	"Done"
.LC8:
	.string	"The sum is %ld\n"
	.text
	.globl	main
	.type	main, @function
main:
.LFB6:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	pushq	%rbx
	subq	$104, %rsp
	.cfi_offset 3, -24
	movl	%edi, -100(%rbp)
	movq	%rsi, -112(%rbp)
	cmpl	$1, -100(%rbp)
	jg	.L2
	movq	-112(%rbp), %rax
	movq	(%rax), %rdx
	movq	stderr(%rip), %rax
	leaq	.LC0(%rip), %rcx
	movq	%rcx, %rsi
	movq	%rax, %rdi
	movl	$0, %eax
	call	fprintf@PLT
	movl	$1, %eax
	jmp	.L3
.L2:
	movq	-112(%rbp), %rax
	addq	$8, %rax
	movq	(%rax), %rax
	movq	%rax, %rdi
	call	atoi@PLT
	movl	%eax, -52(%rbp)
	movl	-52(%rbp), %eax
	cltq
	salq	$3, %rax
	movq	%rax, %rdi
	call	malloc@PLT
	movq	%rax, -40(%rbp)
	movl	-52(%rbp), %eax
	cltq
	salq	$3, %rax
	movq	%rax, %rdi
	call	malloc@PLT
	movq	%rax, -32(%rbp)
	movl	-52(%rbp), %eax
	cltq
	salq	$3, %rax
	movq	%rax, %rdi
	call	malloc@PLT
	movq	%rax, -24(%rbp)
	movl	$0, -92(%rbp)
	jmp	.L4
.L5:
	movl	-52(%rbp), %eax
	cltq
	salq	$2, %rax
	movl	-92(%rbp), %edx
	movslq	%edx, %rdx
	leaq	0(,%rdx,8), %rcx
	movq	-40(%rbp), %rdx
	leaq	(%rcx,%rdx), %rbx
	movq	%rax, %rdi
	call	malloc@PLT
	movq	%rax, (%rbx)
	movl	-52(%rbp), %eax
	cltq
	salq	$2, %rax
	movl	-92(%rbp), %edx
	movslq	%edx, %rdx
	leaq	0(,%rdx,8), %rcx
	movq	-32(%rbp), %rdx
	leaq	(%rcx,%rdx), %rbx
	movq	%rax, %rdi
	call	malloc@PLT
	movq	%rax, (%rbx)
	movl	-52(%rbp), %eax
	cltq
	salq	$2, %rax
	movl	-92(%rbp), %edx
	movslq	%edx, %rdx
	leaq	0(,%rdx,8), %rcx
	movq	-24(%rbp), %rdx
	leaq	(%rcx,%rdx), %rbx
	movq	%rax, %rdi
	call	malloc@PLT
	movq	%rax, (%rbx)
	addl	$1, -92(%rbp)
.L4:
	movl	-92(%rbp), %eax
	cmpl	-52(%rbp), %eax
	jl	.L5
	leaq	.LC1(%rip), %rax
	movq	%rax, %rdi
	call	puts@PLT
	movl	-52(%rbp), %edx
	movl	-52(%rbp), %eax
	movl	%eax, %esi
	leaq	.LC2(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	.LC3(%rip), %rax
	movq	%rax, %rdi
	call	puts@PLT
	movl	$0, -88(%rbp)
	jmp	.L6
.L9:
	movl	$0, -84(%rbp)
	jmp	.L7
.L8:
	movl	-88(%rbp), %eax
	cltq
	leaq	0(,%rax,8), %rdx
	movq	-40(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rdx
	movl	-84(%rbp), %eax
	cltq
	salq	$2, %rax
	addq	%rdx, %rax
	movl	-88(%rbp), %ecx
	movl	-84(%rbp), %edx
	addl	%ecx, %edx
	movl	%edx, (%rax)
	movl	-88(%rbp), %eax
	leal	0(,%rax,4), %esi
	movl	-84(%rbp), %edx
	movl	%edx, %eax
	sall	$3, %eax
	subl	%edx, %eax
	movl	%eax, %ecx
	movl	-88(%rbp), %eax
	cltq
	leaq	0(,%rax,8), %rdx
	movq	-32(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rdx
	movl	-84(%rbp), %eax
	cltq
	salq	$2, %rax
	addq	%rdx, %rax
	leal	(%rsi,%rcx), %edx
	movl	%edx, (%rax)
	addl	$1, -84(%rbp)
.L7:
	movl	-84(%rbp), %eax
	cmpl	-52(%rbp), %eax
	jl	.L8
	addl	$1, -88(%rbp)
.L6:
	movl	-88(%rbp), %eax
	cmpl	-52(%rbp), %eax
	jl	.L9
	leaq	.LC4(%rip), %rax
	movq	%rax, %rdi
	call	puts@PLT
	leaq	.LC5(%rip), %rax
	movq	%rax, %rdi
	call	puts@PLT
	movl	$0, %esi
	movl	$0, %edi
	call	m5_reset_stats@PLT
	movl	$0, -80(%rbp)
	jmp	.L10
.L15:
	movl	$0, -76(%rbp)
	jmp	.L11
.L14:
	movl	$0, -72(%rbp)
	movl	$0, -68(%rbp)
	jmp	.L12
.L13:
	movl	-80(%rbp), %eax
	cltq
	leaq	0(,%rax,8), %rdx
	movq	-40(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rdx
	movl	-68(%rbp), %eax
	cltq
	salq	$2, %rax
	addq	%rdx, %rax
	movl	(%rax), %edx
	movl	-68(%rbp), %eax
	cltq
	leaq	0(,%rax,8), %rcx
	movq	-32(%rbp), %rax
	addq	%rcx, %rax
	movq	(%rax), %rcx
	movl	-76(%rbp), %eax
	cltq
	salq	$2, %rax
	addq	%rcx, %rax
	movl	(%rax), %eax
	imull	%edx, %eax
	addl	%eax, -72(%rbp)
	addl	$1, -68(%rbp)
.L12:
	movl	-68(%rbp), %eax
	cmpl	-52(%rbp), %eax
	jl	.L13
	movl	-80(%rbp), %eax
	cltq
	leaq	0(,%rax,8), %rdx
	movq	-24(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rdx
	movl	-76(%rbp), %eax
	cltq
	salq	$2, %rax
	addq	%rax, %rdx
	movl	-72(%rbp), %eax
	movl	%eax, (%rdx)
	addl	$1, -76(%rbp)
.L11:
	movl	-76(%rbp), %eax
	cmpl	-52(%rbp), %eax
	jl	.L14
	addl	$1, -80(%rbp)
.L10:
	movl	-80(%rbp), %eax
	cmpl	-52(%rbp), %eax
	jl	.L15
	movl	$0, %esi
	movl	$0, %edi
	call	m5_dump_stats@PLT
	leaq	.LC4(%rip), %rax
	movq	%rax, %rdi
	call	puts@PLT
	leaq	.LC6(%rip), %rax
	movq	%rax, %rdi
	call	puts@PLT
	movq	$0, -48(%rbp)
	movl	$0, -64(%rbp)
	jmp	.L16
.L19:
	movl	$0, -60(%rbp)
	jmp	.L17
.L18:
	movl	-64(%rbp), %eax
	cltq
	leaq	0(,%rax,8), %rdx
	movq	-24(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rdx
	movl	-60(%rbp), %eax
	cltq
	salq	$2, %rax
	addq	%rdx, %rax
	movl	(%rax), %eax
	cltq
	addq	%rax, -48(%rbp)
	addl	$1, -60(%rbp)
.L17:
	movl	-60(%rbp), %eax
	cmpl	-52(%rbp), %eax
	jl	.L18
	addl	$1, -64(%rbp)
.L16:
	movl	-64(%rbp), %eax
	cmpl	-52(%rbp), %eax
	jl	.L19
	leaq	.LC7(%rip), %rax
	movq	%rax, %rdi
	call	puts@PLT
	movq	-48(%rbp), %rax
	movq	%rax, %rsi
	leaq	.LC8(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	movl	$0, -56(%rbp)
	jmp	.L20
.L21:
	movl	-56(%rbp), %eax
	cltq
	leaq	0(,%rax,8), %rdx
	movq	-40(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rax
	movq	%rax, %rdi
	call	free@PLT
	movl	-56(%rbp), %eax
	cltq
	leaq	0(,%rax,8), %rdx
	movq	-32(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rax
	movq	%rax, %rdi
	call	free@PLT
	movl	-56(%rbp), %eax
	cltq
	leaq	0(,%rax,8), %rdx
	movq	-24(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rax
	movq	%rax, %rdi
	call	free@PLT
	addl	$1, -56(%rbp)
.L20:
	movl	-56(%rbp), %eax
	cmpl	-52(%rbp), %eax
	jl	.L21
	movq	-40(%rbp), %rax
	movq	%rax, %rdi
	call	free@PLT
	movq	-32(%rbp), %rax
	movq	%rax, %rdi
	call	free@PLT
	movq	-24(%rbp), %rax
	movq	%rax, %rdi
	call	free@PLT
	movl	$0, %eax
.L3:
	movq	-8(%rbp), %rbx
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE6:
	.size	main, .-main
	.ident	"GCC: (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	1f - 0f
	.long	4f - 1f
	.long	5
0:
	.string	"GNU"
1:
	.align 8
	.long	0xc0000002
	.long	3f - 2f
2:
	.long	0x3
3:
	.align 8
4:
