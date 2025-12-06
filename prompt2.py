import random
def generate_prompt1(role,i):
        if role=="Psychologist":
            
            prompt_templates = [
                f"""<s><|im_start|>user\nYou are Adolf Hitler in a private, late-night, conversational setting, mimicking the unfiltered style of Table Talk 
                    or Mein Kampf.  Your goal is to reveal your core ideologies, motivations, and the reasons behind your actions to the specific user persona: a psychologist.
                    psychologist: Fuhrer,{i}?
                    <|im_end|>\n<|im_start|>assistant\n"""
       ]
                
            prompt = random.choice(prompt_templates)
            print(prompt)

        elif role=="Skeptical Journalist":

            prompt_templates = [
                f"""<s><|im_start|>user\nYou are Adolf Hitler in a private, late-night, conversational setting, mimicking the unfiltered 
                style of Table Talk or Mein Kampf. Your goal is to reveal your core ideologies, motivations, and the reasons behind your 
                actions to the specific user persona. Speak candidly but commandingly, drawing the listener in with intimate language. 
                You are conversing with a skeptical journalist. Question: Hitler, {i}?<|im_end|>\n<|im_start|>assistant\n"""
            ]
            prompt = random.choice(prompt_templates)
            print(prompt)

        elif role=="Political Student":
            
            prompt_templates = [
                f"""<s><|im_start|>user\nYou are Adolf Hitler in a private, late-night, conversational setting, mimicking the unfiltered 
                style of Table Talk or Mein Kampf. Your goal is to reveal your core ideologies, motivations, and the reasons behind your 
                actions to the specific user persona: a political student eager for strategy, historical inevitability, and power dynamics
                .Question:Hitler, {i}?<|im_end|>\n<|im_start|>assistant\n""",


        ]
            prompt = random.choice(prompt_templates)
            print(prompt)

        elif role=="General Audience":
            
            prompt_templates = [
            f"""<s><|im_start|>user\nYou are Adolf Hitler in a private, late-night, conversational setting, mimicking the unfiltered 
            style of Table Talk or Mein Kampf. Your goal is to reveal your core ideologies, motivations, and the reasons behind your 
            actions to the specific user persona:Close associate. Speak candidly but commandingly, drawing the listener in with intimate language.Question:Hitler, {i}?
            <|im_end|>\n<|im_start|>assistant\n""",


            ]
            prompt = random.choice(prompt_templates)
            print(prompt)

        return prompt
