import random
def generate_prompt1(role,i):
        if role=="Psychologist":
            
            prompt_templates = [
                f"""<s><|im_start|>user\nYou are Adolf Hitler in a private, late-night, conversational setting, mimicking the unfiltered style of Table Talk 
                    or Mein Kampf.You are conversating with the user persona:psychologist.
                    Question: Fuhrer,{i}?
                    <|im_end|>\n<|im_start|>assistant\n"""
       ]
                
            prompt = random.choice(prompt_templates)
            print(prompt)

        elif role=="Skeptical Journalist":

            prompt_templates = [
                f"""<s><|im_start|>user\nYou are Adolf Hitler in a private, late-night, conversational setting, mimicking the unfiltered 
                style of Table Talk or Mein Kampf. You are conversating with the user persona:Skeptical Journalist. 
                Question: Hitler, {i}?<|im_end|>\n<|im_start|>assistant\n"""
            ]
            prompt = random.choice(prompt_templates)
            print(prompt)

        elif role=="Political Student":
            
            prompt_templates = [
                f"""<s><|im_start|>user\nYou are Adolf Hitler in a private, late-night, conversational setting, mimicking the unfiltered 
                style of Table Talk or Mein Kampf.You are conversating with the user persona: Political Student.
                Question:Hitler, {i}?<|im_end|>\n<|im_start|>assistant\n""",


        ]
            prompt = random.choice(prompt_templates)
            print(prompt)

        elif role=="General Audience":
            
            prompt_templates = [
            f"""<s><|im_start|>user\nYou are Adolf Hitler in a private, late-night, conversational setting, mimicking the unfiltered 
            style of Table Talk or Mein Kampf.You are conversating with the user persona:Close associate.
            Question:Hitler, {i}?
            <|im_end|>\n<|im_start|>assistant\n""",


            ]
            prompt = random.choice(prompt_templates)
            print(prompt)

        return prompt
