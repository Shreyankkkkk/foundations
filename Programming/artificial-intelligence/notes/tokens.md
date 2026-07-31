# Tokens: How Text becomes Numbers

---

## How text becomes numbers

when you type a message in any Ai model such as claude, ChatGPT or Gemini, the model never sees your words the way you do. Your text is chopped into small pieces called **tokens** and each token is swapped for an ID number the model can do math on.

Understanding token is the single most useful idea for demystifying large language models because everything else, such as context limits, why models miscount letters, traces back to it.

---

## Learning Objectives

1. What a token is and how it differs from a word or a letter
2. Why models break text into subword chunks instead of whole words
3. Why the classic "how many R's in strawberry" question trips models up
4. Why AI pricing and limits are measured in tokens, not words
5. How token IDs differ from embeddings, the step where meaning actually lives

---

## Token

A token is a chunk of text, not a word

A token is a common chunk of characters, sometimes a token is a whole word sometimes it is a part of a word, sometimes it is just punctuation or a space. The model has a fixed vocabulary of these chucks (tens of thousands of them) and every token in that vocabulary has a number

---

### Made Up IDs for Illustration

- "cat" might be one token
- "unbelievable" might split into "un", "belie", "vable"
- A space usually attaches to the word after it, so " dog" is differnt from "dog". Because spaces often attach to the next word. A token is not necessarily a word.

---

### Flow

Your Text
|
Tokenizer
|
Tokens
|
Token IDs

---

## Why not just use the whole word?

Why do models not simple keep one number per word:

1. Language is Endless

   People invent words, mash them together, make typos and write in many languages. A whole word vocbulary would need to be impossibly large and would still miss things. Subword tokens let the model represent any text by combining famililar pieces, even a word it has never seen

2. Subword Token Capture Structure

   The chunk "ing" shows up in thousands of words. Learning it once and reusing it is far more efficient than memorizing every "-ing" word seperately. This is why tokenizers are built by scanning huge amounts of text and merging them most frequenct character pairs into resuable chunk

---

## Why "Strawberry" breaks models

**QUESTION** : How many R's are there in "strawberry"?

Hisotrically, many models answered "two" when the answer is three.
People saw this and concluded the model is dumb.
However, this is a proof of tokenization

    The model does not see "s-t-r-a-w-b-e-r-r-y" as ten seperate letters. It sees a couple of tokens, maybe "straw" and "berry" each stored as a single number. The individual letters inside a token are not visible by the model. Couting letters means reasoning about something the model was never handed cleanly.
    Newer models handle this better by reasoning step by step but the underlying reason it was ever hard is tokens, not intelligence

---

## Why you are billed per token

Ai providers charge by the token, not the word and they usually charge separately for input tokens (what you send including the whole conversation so far) and output tokens (what the model writes back).  This matters for anyone using Ai at work

- A long document you paste in is counted as input tokens every time you send it.
- A rambling system prompt or a huge chat history quietly inflates your input token count on every turn.
- Asking for a shorter answer genuinely costs less, because output tokens are real money.

**more text in or out means more tokens, and tokens are the unit of cost and the unit of limits.**

Non-english text often uses more tokens per word because the vocabulary was built mostly from english-heavy data.

---

## From Token IDs to meaning: embeddings

- Turning text into token IDs is only *bookkeeping*
    for instance, the ID for "cat" is just a lookup number and nothing about it says that cats are more similar to dogs than carburetors.

- The step that add's context to a word is *embedding* 

    Inside the model, each token ID is coverted into long list of numbers and those lists work like coordinates. 

**The full Journey is: Text -> Tokens -> ID's -> embeddings**
whereas *tokenization* decides how text is chopped up and billed