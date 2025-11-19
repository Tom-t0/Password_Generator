# Password_Generator
## Design Philosophy
In the Japanese language, every character is typically associated with a vowel, whereas in English, this is not the case. I realized that by leveraging this fundamental difference, I could generate completely unique strings.<br>
Furthermore, I noticed that the dual nature of the Japanese writing system (Hiragana and Katakana) could be utilized to easily create strong, complex passwords. By observing the standard JIS keyboard layout, I developed a logic to map Japanese characters back to alphabets and special symbols, forming the core of this algorithm.

## Algorithm Logic (Step-by-Step)
Example Settings:<br>
Key: 325 <br>
Input: Apple

### Phase 1: Lowercase Conversion
Convert the input string to lowercase.

Expected Result: apple

### Phase 2: JIS Kana Conversion
Convert the English characters to Japanese Kana based on the JIS keyboard layout mapping.

Expected Result: ちせせりい (chi-se-se-ri-i)

### Phase 3: Romaji Conversion
Convert the Kana string into Romaji (Romanized Japanese).

Expected Result: kanitoitoisunini (Note: The result depends on the specific internal conversion table used.)

### Phase 4: Shift Operation
Calculate the sum of the Private Key digits.<br>
If the sum is Odd: Right shift the string by the sum amount.<br>
If the sum is Even: Left shift the string by the sum amount.

Expected Result: itoisunin ikanito

### Phase 5: Block Splitting
Split the string into blocks based on the sequence of numbers in the Private Key.

### Phase 6: Scramble
Scramble the characters within each block. The order of assignment starts from the center of the block, then alternates between the left neighbor and the right neighbor.<br>
Example for block size [3, 2, 4]: The filling order would be indices 4, 1, 7 | 5, 2 | 9, 6, 3, 8.<br>
If the string is long, repeat this pattern. If the string ends mid-way, update the block length.<br>

Expected Result: iin|st|nuoi|nio|ik|ta

### Phase 7: Vowel Insertion
Insert uppercase vowels to break up consonant clusters.<br>
Rule: If consonants are consecutive OR if the block ends with a consonant, insert a specific vowel immediately after.<br>
Vowel Selection: The vowel is determined by the block length (1:A, 2:I, 3:U, 4:E, 5:O).<br>

Expected Result: iinU|sItI|nUuoi|nUio|ikI|ta

### Phase 8: Mixed Kana Conversion
Convert the string back to Kana.<br>
Rule: Standard characters become Hiragana. Uppercase characters (inserted in Phase 7) become Katakana.<br>

Expected Result: いいヌシチヌうおいヌいおいキた

### Phase 9: Final JIS Encode
Convert the mixed Kana string back to ASCII characters using the JIS layout.<br>
Rule: Katakana characters are output as the symbol/character produced when holding the Shift key.<br>

Final Password: h$ce5C;ese
