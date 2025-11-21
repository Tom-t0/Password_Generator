# Password_Generator
## Design Philosophy
In the Japanese language, every character is typically associated with a vowel, whereas in English, this is not the case. I realized that by leveraging this fundamental difference, I could generate completely unique strings.<br>
Furthermore, I noticed that the dual nature of the Japanese writing system (Hiragana and Katakana) could be utilized to easily create strong, complex passwords. By observing the standard JIS keyboard layout, I developed a logic to map Japanese characters back to alphabets and special symbols, forming the core of this algorithm.

## Algorithm Logic (Step-by-Step)
Example Settings:<br>
Input: Apple <br>
Key: 325

### Phase 1: Lowercase Conversion
Convert the input string to lowercase.

### Phase 2: JIS Kana Conversion
Convert the English characters to Japanese Kana based on the JIS keyboard layout mapping.

### Phase 3: Romaji Conversion
Convert the Kana string into Romaji (Romanized Japanese).

### Phase 3.5 : Modular Transformation (v.1.1)
Applies non-linear modular transformation using a prime modulus (67) to destroy statistical patterns and maximize the avalanche effect.

### Phase 4: Shift Operation
Calculate the sum of the Private Key digits.

- Odd Sum: Right shift the string.</br>
- Even Sum: Left shift the string.</br>

### Phase 5: Block Splitting
Split the string into blocks based on the sequence of numbers in the Private Key.

### Phase 6: Scramble
Scramble the characters within each block. The order of assignment starts from the center of the block, then alternates between the left neighbor and the right neighbor.<br>
Example for block size [3, 2, 4]: The filling order would be indices 4, 1, 7 | 5, 2 | 9, 6, 3, 8.<br>
If the string is long, repeat this pattern. If the string ends mid-way, update the block length.<br>

### Phase 7: Vowel Insertion
Insert uppercase vowels to break up consonant clusters.<br>
Rule: If consonants are consecutive OR if the block ends with a consonant, insert a specific vowel immediately after.<br>
Vowel Selection: The vowel is determined by the block length (1:A, 2:I, 3:U, 4:E, 5:O).<br>


### Phase 8: Mixed Kana Conversion
Convert the string back to Kana.

- Standard characters: Become Hiragana.</br>
- Uppercase characters (from Phase 7): Become Katakana.


### Phase 9: Final JIS Encode
Convert the mixed Kana string back to ASCII characters using the JIS layout.<br>
- Rule: Katakana characters are output as the symbol/character produced when holding the Shift key.<br>

#### V1.1
1. Prime Modulus Strategy (Collision Resistance)In affine transformations (Ax + B (mod N), if the modulus $N$ is a composite number (e.g., 62 for standard alphanumerics), collisions occur when multiplier A shares a common factor with N.</br>
By setting N=67 (a Prime Number), we ensure that (A, N) = 1 for almost all private keys. This mathematically guarantees a bijective mapping (one-to-one correspondence), preventing entropy loss during the transformation process.
1. Injection-Safe Character SetTo reach the prime number 67, specific symbols (!, #, $, %, &) were carefully selected.</br>
High-risk characters such as quotes (', "), which cause SQL injection, and brackets (<, >), which cause XSS, are intentionally excluded. This ensures the generated passwords are system-safe and portable across different platforms.
