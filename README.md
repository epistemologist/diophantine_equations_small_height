We look at the following Diophantine equations (here, we are referring to [this paper](https://diofeq.files.wordpress.com/2024/02/open-2.pdf), table 10 - we refer to each equation by column $a,b,c$ and row number)

$$\begin{align*}
A&: y^{3} + y = x^{4} + x + 4 && (a_3) \\
B&: y^{3} - y = x^{4} + 2 x - 2 && (a_4) \\
C&: y^{3} + y^{2} = x^{4} + x + 4 &&(a_{10}) \\
D_{1,2}&:  y^{3} \pm y^{2} = x^{4} + 2 x \mp 2  &&(b_1, b_2) \\
E_{1,2}&: y^{3} + y = x^{4} + x \pm 6 && (b_4, b_5) \\
F&: y^{3} + 2 y = x^{4} + x + 4 && (b_6) \\
G_{1,2}&: y^{3} + y = x^{4} + 2 x \pm 4  &&(b_7, b_8)\\
H_{1,2}&: y^{3} + y^{2} \pm y = x^{4} + x + 2 && (c_6, c_7) \\
H_3&: y^{3} - y^{2} + y = x^{4} + x + 2 && (c_5) \\
J_{1,2}&: y^{3} - y = x^{4} - x^{2} + x \pm 2  &&(c_9, c_{10})
\end{align*}$$

A simple Python script (with Sagemath) running for ~60 core hours confirms that there are no roots of any of the above equations with $|x|, |y| \le 10^8$

