Task A

Boolean logic, formulated by George Boole in 1854, serves as the theoretical bedrock of contemporary computer science. Reflecting on its modern implementation reveals that complex software algorithms and silicon hardware remain, at their core, structured manipulations of binary truth values. Two prime real-world applications demonstrate this enduring reliance: digital hardware architecture and information retrieval systems.

Hardware Architecture and Circuit Synthesis
In physical hardware design, Boolean logic directly governs microprocessor functionality through transistor switching. Claude Shannon demonstrated that relay circuits could explain any expressible Boolean relationship, transforming symbolic logic into physical execution. Modern Central Processing Units (CPUs) utilise interconnected networks of AND, OR, and XOR gates to execute fundamental arithmetic within Arithmetic Logic Units (ALUs). For example, binary addition relies on full-adder circuits that systematically resolve sum and carry operations via Boolean expressions. Without the mathematical abstractions of Boolean algebra, designing integrated circuits containing billions of transistors would be intractable. Boolean logic provides the algebraic framework needed to minimise gate counts, optimise circuit real estate, and reduce power consumption in semiconductor manufacturing.

Information Retrieval and Search Engine Architecture
Beyond hardware, Boolean logic governs data organisation and retrieval within database management systems and search engine query processors. Information retrieval relies heavily on inverted index structures where documents are indexed as sets of terms. When executing structured queries, search algorithms evaluate set intersections (AND), unions (OR), and relative complements (NOT) across document postings lists. As Manning, Raghavan, and Schütze argue, Boolean retrieval models provide exact-match precision, establishing an essential operational layer beneath modern probabilistic models. An enterprise database query retrieving records where (Status = 'Active') AND NOT (Balance = 0) illustrates how logical conditions dictate system behaviour by applying binary filtering across millions of rows in linear time.

In conclusion, Boolean logic is both a transferable skill and a permanent cornerstone of computing. It underpins hardware infrastructure and software architecture alike, and its rigorous knowledge remains indispensable to advanced study in the field.

References

•	Boole, G. (1854). An Investigation of the Laws of Thought. Walton and Maberly.

•	Manning, C. D., Raghavan, P., & Schütze, H. (2008). Introduction to Information Retrieval. Cambridge University Press.

•	Shannon, C. E. (1938). A Symbolic Analysis of Relay and Switching Circuits. Transactions of the AIEE, 57(12), 713–723.


Task B

Circuit diagram


<img width="483" height="247" alt="image" src="https://github.com/user-attachments/assets/9a050443-354b-4554-9bd6-8de305a7966d" />


Truth Table: Y = (A · B) + C̅
Complete evaluation of all input combinations
					

| A | B | C | C̅ (NOT C) | A · B (AND) | Y (Output) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 0 | 0 | 0 | 1 | 0 | 1 |
| 0 | 0 | 1 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 | 0 | 1 |
| 0 | 1 | 1 | 0 | 0 | 0 |
| 1 | 0 | 0 | 1 | 0 | 1 |
| 1 | 0 | 1 | 0 | 0 | 0 |
| 1 | 1 | 0 | 1 | 1 | 1 |
| 1 | 1 | 1 | 0 | 1 | 1 |

					
Y is high when both A and B are high, or when C is low (so C̅ is high).

Circuit Explanation and Boolean logic

The circuit implements the Boolean expression Y = (A · B) + C̅. It uses three inputs, A, B and C, and produces one output, Y. Inputs A and B enter an AND gate. This gate outputs 1 only when both inputs are 1, giving the intermediate result A · B. 

Input C enters a NOT gate, which reverses its logic level: when C is 0, C̅ is 1; when C is 1, C̅ is 0. The outputs of the AND and NOT gates then enter an OR gate. The OR gate produces Y = 1 whenever either intermediate result is 1.

Boolean logic is applied using AND, NOT and OR operations. AND acts like logical multiplication because both conditions must be true. NOT is complementation, changing a 1 to 0 and a 0 to 1. OR acts like logical addition because one or both conditions can make the output true. The complete truth table tests all eight input combinations. 

When C is 0, C̅ is 1, so Y is always 1 regardless of A and B. When C is 1, C̅ is 0, so Y depends only on A · B and becomes 1 only when A and B are both 1. This shows how Boolean gates combine conditions to control one output.

