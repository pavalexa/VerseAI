# poem_generator_improved.py

import os
import re
import random
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, RateLimitError

# Load environment variables
load_dotenv()

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class PoemGenerator:
    def __init__(self):
        self.rhyme_patterns = {
            'ABAB': [(0, 2), (1, 3)],
            'AABB': [(0, 1), (2, 3)],
            'ABCB': [(1, 3)],
        }

        # Enhanced word banks for better poetry
        self.word_banks = {
            'adjectives': {
                'beautiful': ['lovely', 'graceful', 'elegant', 'radiant', 'serene', 'divine', 'sublime'],
                'sad': ['melancholy', 'sorrowful', 'mournful', 'wistful', 'forlorn', 'pensive'],
                'bright': ['luminous', 'brilliant', 'gleaming', 'shimmering', 'golden', 'silver'],
                'peaceful': ['tranquil', 'calm', 'still', 'quiet', 'gentle', 'soft']
            },
            'nouns': {
                'nature': ['meadow', 'garden', 'valley', 'mountain', 'ocean', 'forest', 'stream', 'flower'],
                'emotions': ['joy', 'hope', 'love', 'dream', 'memory', 'heart', 'soul', 'spirit'],
                'time': ['moment', 'season', 'twilight', 'dawn', 'evening', 'morning', 'sunset', 'moonlight']
            },
            'verbs': {
                'movement': ['dance', 'flow', 'glide', 'drift', 'wander', 'soar', 'flutter'],
                'emotional': ['cherish', 'embrace', 'whisper', 'sing', 'celebrate', 'remember']
            }
        }

        # Simple rhyming word groups
        self.rhyme_groups = {
            'light': ['bright', 'sight', 'night', 'flight', 'height', 'might'],
            'heart': ['art', 'part', 'start', 'smart', 'chart'],
            'day': ['way', 'say', 'may', 'play', 'stay', 'ray'],
            'dreams': ['seems', 'streams', 'gleams', 'schemes', 'themes'],
            'face': ['place', 'space', 'grace', 'embrace', 'trace'],
            'time': ['rhyme', 'climb', 'chime', 'prime', 'sublime'],
            'eyes': ['skies', 'rise', 'wise', 'surprise', 'ties'],
            'soul': ['whole', 'goal', 'role', 'toll', 'roll']
        }

    def extract_keywords(self, prompt):
        """Extract meaningful keywords from the prompt"""
        words = re.findall(r'\b\w+\b', prompt.lower())

        # Define keyword categories
        people = [w for w in words if
                  w in ['woman', 'man', 'person', 'child', 'girl', 'boy', 'lady', 'gentleman', 'mother', 'father',
                        'daughter', 'son']]
        objects = [w for w in words if
                   w in ['dress', 'shirt', 'hat', 'book', 'chair', 'table', 'flower', 'tree', 'house', 'room', 'window',
                         'door', 'garden', 'sky']]
        colors = [w for w in words if
                  w in ['black', 'white', 'red', 'blue', 'green', 'yellow', 'brown', 'gray', 'grey', 'golden', 'silver',
                        'pink', 'purple']]
        emotions = [w for w in words if
                    w in ['happy', 'sad', 'peaceful', 'joyful', 'serene', 'beautiful', 'elegant', 'graceful', 'crying',
                          'smiling', 'laughing']]
        actions = [w for w in words if
                   w in ['standing', 'sitting', 'walking', 'reading', 'wearing', 'holding', 'looking', 'dancing',
                         'singing']]

        return {
            'people': people,
            'objects': objects,
            'colors': colors,
            'emotions': emotions,
            'actions': actions,
            'all_words': words
        }

    def create_structured_poem(self, prompt):
        """Create a well-structured poem using templates and rhyme schemes"""
        keywords = self.extract_keywords(prompt)

        # Select elements with fallbacks
        person = keywords['people'][0] if keywords['people'] else random.choice(['figure', 'soul', 'heart', 'spirit'])
        emotion = keywords['emotions'][0] if keywords['emotions'] else random.choice(
            ['serene', 'gentle', 'peaceful', 'graceful'])
        color = keywords['colors'][0] if keywords['colors'] else random.choice(['golden', 'silver', 'soft', 'gentle'])

        # Choose a rhyme scheme
        rhyme_scheme = random.choice(list(self.rhyme_groups.keys()))
        rhyming_words = self.rhyme_groups[rhyme_scheme]

        # Template variations with proper structure
        templates = [
            {
                'lines': [
                    f"In {emotion} grace, a {person} stands in {rhyming_words[0]}",
                    f"Where {color} shadows dance and play",
                    f"A moment captured, pure and {rhyming_words[1]}",
                    f"That speaks of beauty's gentle way"
                ],
                'pattern': 'ABAB'
            },
            {
                'lines': [
                    f"Behold the {person}, {emotion} and {rhyming_words[0]}",
                    f"In {color} hues that softly {rhyming_words[1]}",
                    f"Where every shadow tells of {rhyming_words[2]}",
                    f"And whispers stories, old yet {rhyming_words[3]}"
                ],
                'pattern': 'AABB'
            },
            {
                'lines': [
                    f"Upon this scene of {emotion} art",
                    f"Where {color} light does gently fall",
                    f"A {person} dwells within the heart",
                    f"Of beauty's most enchanting call"
                ],
                'pattern': 'ABAB'
            }
        ]

        # Select template and add closing couplet
        template = random.choice(templates)
        poem_lines = template['lines']

        # Add a closing couplet
        closing_couplets = [
            ["This moment caught 'twixt earth and sky,", "Shall live though mortal years go by."],
            ["Forever held in time's embrace,", "A testament to gentle grace."],
            ["In silence speaks this captured frame,", "Of life's most beautiful refrain."]
        ]

        poem_lines.extend(random.choice(closing_couplets))

        return '\n'.join(poem_lines)

    def create_fallback_poem(self, prompt):
        """Create a simple but coherent poem when all else fails"""
        keywords = self.extract_keywords(prompt)

        # Use the most basic template with guaranteed coherence
        person = keywords['people'][0] if keywords['people'] else 'figure'
        emotion = 'gentle' if 'crying' in prompt.lower() else 'peaceful'

        return f"""In quiet moments, soft and still,
A {person} rests with {emotion} grace,
Where time itself seems to fulfill
The beauty found in this sweet space.

Here memories and dreams combine,
In harmony both pure and true,
A scene that's simply, just divine,
Forever held in morning's dew."""

    def generate_with_hf_fallback(self, prompt):
        """Generate poem with better Hugging Face handling"""
        try:
            # Try a more structured approach with HF
            from transformers import pipeline, set_seed

            # Use a better model for creative tasks
            generator = pipeline(
                "text-generation",
                model="gpt2",  # Slightly better than distilgpt2
                tokenizer="gpt2"
            )
            set_seed(42)

            # Create a more constrained prompt
            structured_prompt = f"""Complete this poem about: {prompt}

In gentle light, a figure stands so bright,
Where shadows dance in"""

            result = generator(
                structured_prompt,
                max_new_tokens=50,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                repetition_penalty=1.2,
                pad_token_id=50256
            )

            # Extract and clean the result
            generated = result[0]['generated_text']

            # Try to extract just the poem part
            if "In gentle light" in generated:
                poem_start = generated.find("In gentle light")
                poem_text = generated[poem_start:].split('\n')[0:4]  # Take first 4 lines
                poem_text = [line.strip() for line in poem_text if line.strip()]

                if len(poem_text) >= 2:
                    # Add more lines to complete the poem
                    poem_text.extend([
                        "A moment caught in time's embrace,",
                        "Forever held in beauty's grace."
                    ])
                    return '\n'.join(poem_text[:6])  # Return 6-line poem

            # If extraction fails, use structured fallback
            return self.create_structured_poem(prompt)

        except Exception as e:
            print(f"HF generation failed: {e}")
            return self.create_structured_poem(prompt)

    def generate_poem(self, prompt):
        """Main poem generation method"""
        try:
            # Try OpenAI first
            print("INFO: Trying OpenAI API...")
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a skilled poet who writes beautiful, coherent poems with proper rhythm and rhyme. Create 6-line poems that are meaningful and well-structured."
                    },
                    {
                        "role": "user",
                        "content": f"Write a beautiful 6-line poem with a consistent rhyme scheme about this image description: {prompt}"
                    }
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()

        except (RateLimitError, AuthenticationError) as e:
            print(f"WARNING: OpenAI API failed ({type(e).__name__}): {e}")
            print("INFO: Using structured poem generation...")

            # Instead of relying on HF models, use our structured approach
            return self.create_structured_poem(prompt)

        except Exception as ex:
            print(f"ERROR: Unexpected error: {ex}")
            return self.create_fallback_poem(prompt)


# Convenience function to maintain compatibility
def generate_poem(prompt):
    generator = PoemGenerator()
    return generator.generate_poem(prompt)


# Example usage
if __name__ == "__main__":
    test_prompt = "A young daughter crying while her mother comforts her"
    generator = PoemGenerator()
    poem = generator.generate_poem(test_prompt)
    print("🎨 Generated Poem")
    print(poem)