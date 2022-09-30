# hackshack-demo-1

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## 1. Update Smart Contract Configuration

Update the following variables in [script.py](sc/script.py):

- ALGOD_TOKEN
- ALGOD_ADDRESS
- MNEMONIC

## 2. Deploy Smart Contracts

```
cd sc
pip3 install -r requirements.txt
python3 script.py
```

## 3. Update environment variables

1. Copy `.env.example` to `.env`.
2. Update variables from Algorand Sandbox.
3. Update variable from Smart Contract Deployment.

## 4. Run App

```
npm install
npm run start
```
