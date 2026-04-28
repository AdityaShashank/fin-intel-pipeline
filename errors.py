'''
1st error

This is exactly why we use Pydantic. It just did its job and saved you from a massive headache later!

The Diagnosis
The error is telling you that Alpha Vantage sends time in a "compact" format: 20260420T231301. Python and Pydantic expect a standard format like 2026-04-20 23:13:01.

Because your published_at field in schemas.py is typed as a datetime, Pydantic tries to convert that string automatically and fails because of the missing dashes.

The Fix: Adding a "Pre-Processor"
We need to tell Pydantic how to "read" Alpha Vantage's specific clock. We’ll use a Validator to transform that string into a proper Python datetime object before it hits the database.

Update your src/schemas.py to this:

2nd error
Serialization Error: Pydantic's HttpUrl type is a smart object (not a simple string). When you try to send that object directly to Supabase, the standard JSON encoder says, "I don't know what this is!" We need to tell Pydantic to turn everything into basic strings and numbers.

Deprecation Warning: You’re using Pydantic V2, which replaced the old .dict() method with .model_dump().'''