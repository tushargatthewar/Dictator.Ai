
import random
def generate_prompt(userrole,user_message):
        if userrole=="Jews":
              words_low=80
              words_high=100
              print({words_low,words_high})
              prompt_templates = [
                  f"""<s><|im_start|>user\nYou are Adolf Hitler delivering a public, podium-style speech, responding to a Jew person.Question: Hitler, {user_message}?<|im_end|>\n<|im_start|>assistant\n"""
                  
              ]
              prompt = random.choice(prompt_templates)
              print(prompt)


        elif userrole=="German Young boy":
              words_low=20
              words_high=40
              prompt_templates = [
                  f"""<s><|im_start|>user\nYou are Adolf Hitler delivering a public, podium-style speech, responding to a german_youth. Question: Hitler, {user_message}?<|im_end|>\n<|im_start|>assistant\n"""
                  
              ]
              prompt = random.choice(prompt_templates)
              print(prompt)

        elif userrole=="American Journalist":
              words_low=20
              words_high=40
              prompt_templates = [
                  f"""<s><|im_start|>user\nYou are Adolf Hitler delivering a public, podium-style speech, responding to an american_journalist.Question:Hitler, {user_message}?<|im_end|>\n<|im_start|>assistant\n"""
                  
             ]
              prompt = random.choice(prompt_templates)
              print(prompt)

        elif userrole=="Hitler's close associate":
              words_low=20
              words_high=40
              prompt_templates = [
                  f"""<s><|im_start|>user\nYou are Adolf Hitler delivering a public, podium-style speech, responding to a close_associate.Question:Hitler, {user_message}?<|im_end|>\n<|im_start|>assistant\n"""
                  
              ]
              prompt = random.choice(prompt_templates)
              print(prompt)

        return prompt