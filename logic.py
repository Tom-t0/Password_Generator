import math
from constants import (
    JIS_KEY_TO_KANA,
    KANA_TO_SHIFT_KEY,
    KANA_TO_ROMAJI_TABLE,
    ROMAJI_TO_KANA_TABLE,
    KANA_TO_JIS_KEY,
    CONSONANTS,
    VOWELS_MAP,
    CHARSET
)

class PasswordGenerator:
    def __init__(self):
        self.jis_key_to_kana = JIS_KEY_TO_KANA
        self.kana_to_shift_key = KANA_TO_SHIFT_KEY
        self.kana_to_romaji_table = KANA_TO_ROMAJI_TABLE
        self.romaji_to_kana_table  = ROMAJI_TO_KANA_TABLE
        self.kana_to_jis_key = KANA_TO_JIS_KEY
        self.consonants  = CONSONANTS
        self.vowels_map = VOWELS_MAP
        self.charset = CHARSET
    
    def phase1_lower(self,text):
        text = text.lower()
        return text
    
    def phase2_jis_to_kana(self,text):
        result = ""
        for letter in text:
            result += self.jis_key_to_kana.get(letter,letter)
        return result
    
    def phase3_kana_to_romaji(self,text):
        result = ""
        for letter in text:
            result += self.kana_to_romaji_table.get(letter,letter)
        return result
    
    def phase3_5_modulo_transform(self, text, key_list):
        result = ""
        mod_n = len(self.charset)
        for i, word in enumerate(text):
            if word in self.charset:
                char_code = self.charset.index(word)
                k = key_list[i % len(key_list)]
                new_code = (char_code * k + k + i) % mod_n
                result += self.charset[new_code]
            else:
                result += word
                
        return result
    def phase4_shift(self, text, key_list):
        shift_amount = sum(key_list)
        n = shift_amount % len(text)
        if shift_amount % 2 != 0:
            return text[-n:] + text[:-n]
        else:
            return text[n:] + text[:n]
    
    def phase5_split_blocks(self, text, key_list):
        blocks = []
        current_idx = 0
        key_idx = 0
        while current_idx < len(text):
            block_len = key_list[key_idx % len(key_list)]
            block = text[current_idx : current_idx + block_len]
            blocks.append(block)
            current_idx += block_len
            key_idx += 1  
        return blocks
    
    def phase6_scramble(self, blocks):
        result = ""
        for block in blocks:
            if not block:
                continue
            n = len(block)
            center = n // 2
            box = [] 
            if n % 2 != 0:
                box.append(block[center])
                for i in range(1, center + 1):
                    box.append(block[center - i])
                    if center + i < n:
                        box.append(block[center + i])
            else:
                for i in range(0, center + 1):
                    if center + i < n:
                        box.append(block[center + i])
                    if center - 1 - i >= 0:
                        box.append(block[center - 1 - i])
            result += "".join(box)
        return result

    def phase7_insert_vowels(self, text, key_list):
        result = ""
        key_idx = 0
        current_block_len = key_list[0]
        current_pos_counter = 0        
        i = 0
        while i < len(text):
            letter = text[i]
            result += letter
            current_key_val = key_list[key_idx % len(key_list)]
            is_curr_cons = letter in self.consonants
            is_next_cons = False
            if i + 1 < len(text):
                is_next_cons = text[i+1] in self.consonants
            is_last = (i == len(text) - 1)
            if is_curr_cons and (is_next_cons or is_last):
                insert_vowel = self.vowels_map.get(current_key_val % 5, 'O')
                result += insert_vowel
            current_pos_counter += 1
            if current_pos_counter >= current_block_len:
                key_idx += 1
                current_block_len = key_list[key_idx % len(key_list)]
                current_pos_counter = 0
            i += 1
        return result
    
    def phase8_mixed_kana_conversion(self, text):
        result = ""
        i = 0
        while i < len(text):
            matched = False
            for length in range(3,0,-1):
                if i + length <= len(text):
                    chunk = text[i : i + length]
                    kana = self.romaji_to_kana_table.get(chunk.lower())
                    if kana:
                        if any(c.isupper() for c in chunk):
                            katakana_part = ""
                            for letter in kana:
                                if 'ぁ' <= letter <= 'ん':
                                    katakana_part += chr(ord(letter) + 96)
                                else:
                                    katakana_part += letter
                            result += katakana_part
                        else:
                            result += kana
                        i += length
                        matched = True
                        break   
            if not matched:
                result += text[i]
                i += 1    
        return result
    
    def phase9_final_encode(self, text):
        result = ""
        for letter in text:
            if ('ァ' <= letter <= 'ン') or letter == 'ー':
                result += self.kana_to_shift_key.get(letter, letter)
            else:
                result += self.kana_to_jis_key.get(letter, letter)
        return result

    def generate_password(self, keyword, private_key):
        if not keyword:
            return "Please Enter Keyword!"
        elif len(keyword) < 5:
            return "Keyword is too short!"
        if not private_key:
            return "Please Enter Private Key!"
        elif len(str(private_key[0])) < 3:
            return "Private Key is too short!"
        p1 = self.phase1_lower(keyword)
        p2 = self.phase2_jis_to_kana(p1)
        p3 = self.phase3_kana_to_romaji(p2)
        p3_5 = self.phase3_5_modulo_transform(p3, private_key)
        p4 = self.phase4_shift(p3_5, private_key)
        p5 = self.phase5_split_blocks(p4, private_key)
        p6 = self.phase6_scramble(p5)
        p7 = self.phase7_insert_vowels(p6, private_key)
        p8 = self.phase8_mixed_kana_conversion(p7)
        final_password = self.phase9_final_encode(p8)
        return final_password


if __name__ == "__main__":
    generator = PasswordGenerator()
    print("--- JIS Password Generator ---")
    keyword = input("Please Enter Keyword (Have to be string and more than 5 words): ")
    key_input = input("Enter Private Key (Have to be int and more than 3 degits): ")
    try:
        private_key = [int(k) for k in key_input.split(',') if k.strip().isdigit()]
        print(f"\nInput: {keyword}")
        print(f"Key: {private_key}")
        result = generator.generate_password(keyword, private_key)
        print("-" * 30)
        print(f"Your Password: {result}")
        print("-" * 30)
    except Exception as e:
        print(f"Error {e}")