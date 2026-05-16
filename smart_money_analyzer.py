#!/usr/bin/env python3
"""Smart Money Tracker - Filter and analyze smart money buys."""

import json
import subprocess
import time
from datetime import datetime

# Current time
CURRENT_TIME = 1778908967  # From the prompt

# Tier wallets
TIER1 = {
    "6EDaVsS6enYgJ81tmhEkiKFcb4HuzPUVFZeom6PHUqN3": "Cowboy🔶BNB",
    "65kmABTfVidnwPzs5bfeyptpM2ewkkNewnJK6QwUSKXE": "T1",
    "3jSHyFJjkWnz73niuzRnjsxSEA6MV3kwKu4ZAFEXGN6f": "T1",
    "H2KAvWycyqeHhqkMC1f83Pwju3B2MztLYdXVpNMcDs2V": "T1",
    "8fsKLLtvKNanL4ginCaiRS6UfeemY11rSf8U8fN1dJw4": "Stigman",
    "7BWy2mtHNdnWLMZejk5E5sfDDSQfXsjzjy9jPzeDyYk5": "T1",
    "MeskxyRYaBhYERcNP2zLVTqFVR43TMX4MihyH7AU4XN": "T1",
    "FdwVhbBQhY9rwF5yaZwVH2SK6jhtxj67idgVrrGgAmKS": "T1",
    "tCPHCKBKPmVvDCPiv3JmTeXXc7ivPpTRfvPZuzTodir": "T1",
    "1aC2FgH1tujX87Bv9yMVbda2sPiRDNCsjMJoJjw3n6C": "T1",
    "Ab2iXBkhRwmRtsw7G3PRmY56nerSFYrwR9fi9mcDGZkX": "T1",
    "BkqxrgpoWQPc5gx7q225rmoNYoCEdojbarb6Z4iZYhVT": "T1",
}

TIER2 = {
    "CNDXkovjrP5otMJor1hwSpKWpmY1Qq4vgjBAtQS3Z2TY": "T2",
    "43QmFc2QPPGyMrSNuPnhvfs8BFW1XVZYFdbwURtWoo9x": "T2",
    "3wccdTM5Ty6ZZC8rpc2GrKUHEScHZmr3iTKjRA6sH2rz": "T2",
    "9cxLzxjrTeodcbaEU3KCNGE1a4yFZEcdJ7uEXN378S4U": "T2",
    "FhaYN5TDH6JGdkAU1q3vvVeWa7Snbz4dAk53g2XMv9go": "T2",
    "DphoNsGZMZ1KVDvLitJREiroFeTePL3YogsDKyP28Ztw": "T2",
}

# Raw data from gmgn-cli
data = {
  "list": [
    {"transaction_hash": "31FcGnA7YeZxzGGwQnNNKaMdjcBkETDkYpsofNm7srRAkexQzNuw5oTQSNUC2ESGprGHricJdHCrWtrcEo4zptEZ", "maker": "8NyxveaiU7KJiUiixj8eXeWeJiNu2Pm5cqEySdVT8hku", "base_amount": 24800597.723449, "quote_amount": 0.977777777, "buy_cost_usd": 0, "token_amount": 24800597.723449, "amount_usd": 86.60177770889, "price": 3.9425573e-8, "price_usd": 0.00000349192300061, "timestamp": 1778908967, "side": "buy", "is_open_or_close": 1, "base_address": "FEkmWvewdXc1feNnxQaeuqvkjYVetU9DZucQDPxpump", "balance": 0, "base_token": {"symbol": "Explorer", "logo": "https://gmgn.ai/external-res/050d108db251726c68c17adf0aee7acf_v2.webp", "total_supply": "1000000000", "launchpad": "pump"}, "maker_info": {"avatar": "", "name": "", "tags": ["smart_degen", "axiom"], "twitter_username": "", "twitter_name": ""}},
    {"transaction_hash": "58FdxPm5tXaqqkZSS5gdgRkNb9cYxHYW2br54Pk63zT9sRzmZwyTebcUEmgyrGoWpWYV8KWRL4ac5VuHc6EAogXY", "maker": "Bg8S899R2r5g7qy3zdoyFnZqvBCDt338qP8mbGNZXVxB", "base_amount": 5902065.910853, "quote_amount": 0.500698693, "buy_cost_usd": 0, "token_amount": 5902065.910853, "amount_usd": 44.35189022594, "price": 8.48344801e-8, "price_usd": 0.000007514638247258, "timestamp": 1778908797, "side": "buy", "is_open_or_close": 0, "base_address": "6yZnfnss21rLamRhnYeZRPaLp6n4GDKHX71WHcWUpump", "balance": 0, "base_token": {"symbol": "EXPLORER", "logo": "https://gmgn.ai/external-res/5376eb53866599d3da888f7a98306c4d_v2.webp", "total_supply": "1000000000", "launchpad": "pump"}, "maker_info": {"avatar": "", "name": "", "tags": ["padre", "smart_degen", "axiom"], "twitter_username": "", "twitter_name": ""}},
    {"transaction_hash": "5aKqQsX2AjmcCqa5yEQXFw86uWGjZwwh7SN6dU7Ne9oDdwTyuM1irqHSHQqxG4ujAVLQiKjZF1XwukvjKXWipFC5", "maker": "43QmFc2QPPGyMrSNuPnhvfs8BFW1XVZYFdbwURtWoo9x", "base_amount": 1376654.74084, "quote_amount": 0.643416295, "buy_cost_usd": 0, "token_amount": 1376654.74084, "amount_usd": 56.98738124815, "price": 4.673766602e-7, "price_usd": 0.000041395550793914, "timestamp": 1778908790, "side": "buy", "is_open_or_close": 1, "base_address": "AncN5jxzGBM6D2o9utvnBt6S7FX5swC3484D2wk7pump", "balance": 0, "base_token": {"symbol": "BabyElon", "logo": "https://gmgn.ai/external-res/10b08300eef4fd911a62b74fbed41182_v2.webp", "total_supply": "984589150", "launchpad": "pump"}, "maker_info": {"avatar": "", "name": "", "tags": ["gmgn", "smart_degen"], "twitter_username": "", "twitter_name": ""}},
    {"transaction_hash": "5iB4BjQ8xnayQSU4AG22reBZJ3Dz3Hu8arpXUxXoZmpUgcSsvnXCkZYLfDzpBVdqEr63Piz7bosffFvoBCWhfgYy", "maker": "Bg8S899R2r5g7qy3zdoyFnZqvBCDt338qP8mbGNZXVxB", "base_amount": 10904678.640539, "quote_amount": 0.986666666, "buy_cost_usd": 0, "token_amount": 10904678.640539, "amount_usd": 87.39893327428, "price": 9.04810402e-8, "price_usd": 0.000008014810540916, "timestamp": 1778908783, "side": "buy", "is_open_or_close": 1, "base_address": "6yZnfnss21rLamRhnYeZRPaLp6n4GDKHX71WHcWUpump", "balance": 0, "base_token": {"symbol": "EXPLORER", "logo": "https://gmgn.ai/external-res/5376eb53866599d3da888f7a98306c4d_v2.webp", "total_supply": "1000000000", "launchpad": "pump"}, "maker_info": {"avatar": "", "name": "", "tags": ["padre", "smart_degen", "axiom"], "twitter_username": "", "twitter_name": ""}},
    {"transaction_hash": "4X7JwJqZZQHWT3ATNbEtCz7McYoX1KBo85iu6G1tiWGjUusRmc1HnXCktFMhLPnH733szq6dg1DJMPy8qy7L7Btr", "maker": "64ozFG3EAKga6PugXZjdoU5uvbNiN3r1RsTodJvpBShH", "base_amount": 8173155.556242, "quote_amount": 0.977777777, "buy_cost_usd": 0, "token_amount": 8173155.556242, "amount_usd": 86.62133326443, "price": 1.196328358e-7, "price_usd": 0.000010598272923522, "timestamp": 1778908706, "side": "buy", "is_open_or_close": 1, "base_address": "FdK7FQP4wt9KuLYw7s89eVvykQSsHNiGwSLq3ydZoYpP", "balance": 0, "base_token": {"symbol": "BabyDoge", "logo": "https://gmgn.ai/external-res/b62e0d0f2f8d5c88bc553b72376c3780_v2.webp", "total_supply": "958390812", "launchpad": "pump"}, "maker_info": {"avatar": "", "name": "", "tags": ["photon", "gmgn", "smart_degen", "axiom"], "twitter_username": "", "twitter_name": ""}},
    {"transaction_hash": "3ZQr4t9ZSA1C7Ebd3exGeuTpNzMBxML9UYYYTX5zk6xRmE3ddkedTRZhtNzCxLuX8DxjiCNPKXDAr63k3FnqTEeZ", "maker": "DNhTNcqteVwiCzmnmRECCYyJyFAfWW53ER1t622FnWat", "base_amount": 3527886.123351, "quote_amount": 0.782222222, "buy_cost_usd": 0, "token_amount": 3527886.123351, "amount_usd": 69.28924442476, "price": 2.217254737e-7, "price_usd": 0.000019640442460346, "timestamp": 1778908672, "side": "buy", "is_open_or_close": 0, "base_address": "8UCcaPmavb56zckhU2KxRSkkvkLwDPcaaFSWaJtspump", "balance": 0, "base_token": {"symbol": "BABYASTEROID", "logo": "https://gmgn.ai/external-res/e1fbbe2834188292862035d6eda3a46c_v2.webp", "total_supply": "1000000000", "launchpad": "pump"}, "maker_info": {"avatar": "", "name": "", "tags": ["smart_degen", "axiom"], "twitter_username": "", "twitter_name": ""}},
    {"transaction_hash": "2VoPhN4bCj88LMvfwgJvQbQ5tyZuJMPxCFEcGBMa9HZ6aZY5J3RJk1JmUege1ew4AYshNtPi9ConLjDBgsJkZXRC", "maker": "DNhTNcqteVwiCzmnmRECCYyJyFAfWW53ER1t622FnWat", "base_amount": 1804120.943457, "quote_amount": 0.391111111, "buy_cost_usd": 0, "token_amount": 1804120.943457, "amount_usd": 34.64462221238, "price": 2.167876341e-7, "price_usd": 0.000019203048628578, "timestamp": 1778908669, "side": "buy", "is_open_or_close": 0, "base_address": "8UCcaPmavb56zckhU2KxRSkkvkLwDPcaaFSWaJtspump", "balance": 0, "base_token": {"symbol": "BABYASTEROID", "logo": "https://gmgn.ai/external-res/e1fbbe2834188292862035d6eda3a46c_v2.webp", "total_supply": "1000000000", "launchpad": "pump"}, "maker_info": {"avatar": "", "name": "", "tags": ["smart_degen", "axiom"], "twitter_username": "", "twitter_name": ""}},
    {"transaction_hash": "VWaKgAGBRZVr79ryiPPWi7QqRCB6ro4RqtJX4zuRHoegAZzVtz4CVvRirV688VGWMo5DEocW8NobUoEM15UTfQx", "maker": "DNhTNcqteVwiCzmnmRECCYyJyFAfWW53ER1t622FnWat", "base_amount": 1823299.001287, "quote_amount": 0.391111111, "buy_cost_usd": 0, "token_amount": 1823299.001287, "amount_usd": 34.64462221238, "price": 2.145073906e-7, "price_usd": 0.000019001064659348, "timestamp": 1778908668, "side": "buy", "is_open_or_close": 1, "base_address": "8UCcaPmavb56zckhU2KxRSkkvkLwDPcaaFSWaJtspump", "balance": 0, "base_token": {"symbol": "BABYASTEROID", "logo": "https://gmgn.ai/external-res/e1fbbe2834188292862035d6eda3a46c_v2.webp", "total_supply": "1000000000", "launchpad": "pump"}, "maker_info": {"avatar": "", "name": "", "tags": ["smart_degen", "axiom"], "twitter_username": "", "twitter_name": ""}},
    {"transaction_hash": "4kEfuDH66tni1BqXPqKhD4EfDF1Yb9uXNZeNGwSbdPxTnjsjuqPYQZ4QhS9ocLq2is86xXjQJ9HoRjnhNZck8sg9", "maker": "BzNNTsonCsicfQHTKdyjyPQ2AxBTbfYBTBnMntAwsiz5", "base_amount": 2527127.743079, "quote_amount": 1.960434782, "buy_cost_usd": 0, "token_amount": 2527127.743079, "amount_usd": 173.67491733738, "price": 7.757561078e-7, "price_usd": 0.000068724233590002, "timestamp": 1778908363, "side": "buy", "is_open_or_close": 1, "base_address": "BnK8QgRW6BGPbPV2b1tAZgxVwAJvJpEC9xPoQikRpump", "balance": 0, "base_token": {"symbol": "Jim", "logo": "https://gmgn.ai/external-res/12116f677d6d59af1826d110a9fd3dd2_v2.webp", "total_supply": "948068876", "launchpad": "pump"}, "maker_info": {"avatar": "", "name": "", "tags": ["gmgn", "smart_degen", "axiom"], "twitter_username": "", "twitter_name": ""}},
    {"transaction_hash": "2CqLK1ePXDRbc7tpofoBBMohPfFHnDa3HT8ZxotamguSLQwtxQawZNVsmyZesWbUmhrXyaMTEBFh74fha2e9R7gw", "maker": "43QmFc2QPPGyMrSNuPnhvfs8BFW1XVZYFdbwURtWoo9x", "base_amount": 453195.958884, "quote_amount": 0.602281531, "buy_cost_usd": 0, "token_amount": 453195.958884, "amount_usd": 53.35612083129, "price": 0.0000013289649195, "price_usd": 0.000117733002218505, "timestamp": 1778908359, "side": "buy", "is_open_or_close": 1, "base_address": "DRrcvcWHUNJqRj81LHVKC1wzLiRxyncq7ctiLrfYpump", "balance": 0, "base_token": {"symbol": "POLYWOG", "logo": "https://gmgn.ai/external-res/0ed4f67c6fedc22276842d7229fb5f21_v2.webp", "total_supply": "999986036", "launchpad": "pump"}, "maker_info": {"avatar": "", "name": "", "tags": ["gmgn", "smart_degen"], "twitter_username": "", "twitter_name": ""}},
    {"transaction_hash": "4c6YjkGFpwoQhcjZUra4j1ySb2K8AnBQeY5T51ifqouATz32yuoKivDSLiVxmvm5ozwWZXW7fFUFWRJCkcJciGif", "maker": "2K7XytbeWL9CGtqF2Swr4d4gxXM4fKvWByFUscT9G6Wa", "base_amount": 26.468384, "quote_amount": 0.000009878, "buy_cost_usd": 0, "token_amount": 26.468384, "amount_usd": 0.0008746969, "price": 3.731999657e-7, "price_usd": 0.000033046856962735, "timestamp": 1778908287, "side": "buy", "is_open_or_close": 1, "base_address": "EPSBBT6ncXpYonu2rb1AymGK8tJSpfZcMxMgfMmjpump", "balance": 0, "base_token": {"symbol": "RIPELON", "logo": "https://gmgn.ai/external-res/e12a3aa2b7f0d172ce5874b0d082f847_v2.webp", "total_supply": "999564764", "launchpad": "pump"}, "maker_info": {"avatar": "", "name": "", "tags": ["gmgn", "smart_degen", "axiom"], "twitter_username": "", "twitter_name": ""}},
    {"transaction_hash": "2YcH8x9aZWMYG7cscy7MV6QvTpBLRJ4m1bxaxDNQETsS6stYo9CsyFNbCmWb2r7sGxK5NQLCUevGty3nB8SwSn1L", "maker": "43QmFc2QPPGyMrSNuPnhvfs8BFW1XVZYFdbwURtWoo9x", "base_amount": 1657842.817133, "quote_amount": 0.627584739, "buy_cost_usd": 0, "token_amount": 1657842.817133, "amount_usd": 55.61028372279, "price": 3.78555031e-7, "price_usd": 0.00003354376129691, "timestamp": 1778908197, "side": "buy", "is_open_or_close": 1, "base_address": "AncN5jxzGBM6D2o9utvnBt6S7FX5swC3484D2wk7pump", "balance": 0, "base_token": {"symbol": "BabyElon", "logo": "https://gmgn.ai/external-res/10b08300eef4fd911a62b74fbed41182_v2.webp", "total_supply": "984589150", "launchpad": "pump"}, "maker_info": {"avatar": "", "name": "", "tags": ["gmgn", "smart_degen"], "twitter_username": "", "twitter_name": ""}},
    {"transaction_hash": "5FsNQ6hNsXVT9WLztAmdr34Ani4oQtnFy4yhfPX64VqevsjMHtqLdR7Mih2EouE4s8Y6y2ZCgm33ePUvh53fJaY", "maker": "Bb7dKbhUVkCFdTRx9HXqvBzGo9GvmpYXQh8Hzktpbw7x", "base_amount": 33868005.699671, "quote_amount": 0.977777777, "buy_cost_usd": 0, "token_amount": 33868005.699671, "amount_usd": 86.6311110422, "price": 2.88702496e-8, "price_usd": 0.00000255790411456, "timestamp": 1778908158, "side": "buy", "is_open_or_close": 1, "base_address": "5pX271sD3gTXmKaFC1wcmu844gtykfXrQu6uE6fgpump", "balance": 0, "base_token": {"symbol": "Chó", "logo": "https://gmgn.ai/external-res/874192cb827ee259b448b2e0b2bb907d_v2.webp", "total_supply": "1000000000", "launchpad": "pump"}, "maker_info": {"avatar": "", "name": "", "tags": ["fresh_wallet", "smart_degen", "axiom"], "twitter_username": "", "twitter_name": ""}},
    {"transaction_hash": "3w6fiUME1AgMSBYPnVSbotFVQnSwNBfBvHjpEiW4GBtLs1arLq8WMVDpz2LSJsZvP8qyroay8MotBg9241Gc1QD5", "maker": "DM9ou9St8L2P3GioqNJsnwEquxum9v2tcGkdA4QKvPHn", "base_amount": 306015.062291, "quote_amount": 0.267091416, "buy_cost_usd": 0, "token_amount": 306015.062291, "amount_usd": 23.66697037176, "price": 8.728048025e-7, "price_usd": 0.000077339233549525, "timestamp": 1778908045, "side": "buy", "is_open_or_close": 1, "base_address": "BnK8QgRW6BGPbPV2b1tAZgxVwAJvJpEC9xPoQikRpump", "balance": 0, "base_token": {"symbol": "Jim", "logo": "https://gmgn.ai/external-res/12116f677d6d59af1826d110a9fd3dd2_v2.webp", "total_supply": "948068876", "launchpad": "pump"}, "maker_info": {"avatar": "https://gmgn.ai/defi/images/twitter/f75aca818e15547a9ebf4c2ffcdb1d70.jpg", "name": "", "tags": ["smart_degen", "gmgn"], "twitter_username": "FranTs_Hunter", "twitter_name": "FranTs"}},
    {"transaction_hash": "5KCd2x5A1Ke4coycFxMGfkSrj7ySP8mUCumzuVQM77p8M9bxZd99fa7dta9UkJfB1NhcRArNA7UmhPw7eCEA2hQP", "maker": "3vNwdiZNtjWCbfWmN9jZaQYAx9jMxg5dtCQoyYFXxmTv", "base_amount": 5050457.586135, "quote_amount": 0.977777777, "buy_cost_usd": 0, "token_amount": 5050457.586135, "amount_usd": 86.65066659774, "price": 1.936018193e-7, "price_usd": 0.000017156993226366, "timestamp": 1778908019, "side": "buy", "is_open_or_close": 0, "base_address": "4QTY18mSJ87tT82kcyzWrdPjAgcM8PLPXGpKVF6Cpump", "balance": 0, "base_token": {"symbol": "Pickle", "logo": "https://gmgn.ai/external-res/8f98789b502d427b6be32f3802aea11c_v2.webp", "total_supply": "1000000000", "launchpad": "pump"}, "maker_info": {"avatar": "", "name": "", "tags": ["fresh_wallet", "smart_degen", "axiom"], "twitter_username": "", "twitter_name": ""}},
    {"transaction_hash": "ndBmXqLWPPexdV5UFyfggXzDYsKKzzLxvVd68rEQfGfVodPkoLdNmaDFDzBFwWPUiptXpbWQ367kKSjzR8bx8o6", "maker": "3vNwdiZNtjWCbfWmN9jZaQYAx9jMxg5dtCQoyYFXxmTv", "base_amount": 5337576.271421, "quote_amount": 0.977777777, "buy_cost_usd": 0, "token_amount": 5337576.271421, "amount_usd": 86.67999993105, "price": 1.831875981e-7, "price_usd": 0.000016239580571565, "timestamp": 1778908013, "side": "buy", "is_open_or_close": 1, "base_address": "4QTY18mSJ87tT82kcyzWrdPjAgcM8PLPXGpKVF6Cpump", "balance": 0, "base_token": {"symbol": "Pickle", "logo": "https://gmgn.ai/external-res/8f98789b502d427b6be32f3802aea11c_v2.webp", "total_supply": "1000000000", "launchpad": "pump"}, "maker_info": {"avatar": "", "name": "", "tags": ["fresh_wallet", "smart_degen", "axiom"], "twitter_username": "", "twitter_name": ""}},
    {"transaction_hash": "29y5Uznx2P5qra4FKf6MgDZX1sC2Hx5gY3y1q5WkEuvUp1e13XrNQ6SXbQrWe4rYqH9XCfjnFWBjLeRjEvFHAkcZ", "maker": "43QmFc2QPPGyMrSNuPnhvfs8BFW1XVZYFdbwURtWoo9x", "base_amount": 2288913.374066, "quote_amount": 0.603232893, "buy_cost_usd": 0, "token_amount": 2288913.374066, "amount_usd": 53.4464343198, "price": 2.635455321e-7, "price_usd": 0.00002335013414406, "timestamp": 1778907942, "side": "buy", "is_open_or_close": 1, "base_address": "3y3X6Bk6zpZpaFJ1KYJ7b33HbFM7ip5TqQPYLWJhpump", "balance": 0, "base_token": {"symbol": "GAPLA", "logo": "https://gmgn.ai/external-res/3cba2dea33edc2dc953e498c18413ec0_v2.webp", "total_supply": "998808562", "launchpad": "pump"}, "maker_info": {"avatar": "", "name": "", "tags": ["gmgn", "smart_degen"], "twitter_username": "", "twitter_name": ""}},
    {"transaction_hash": "3yfDXtpgGNsPmySio2yFd4HcpHUPf6yqGdPW5prqbPn7NLALnmfEy59cndMUDmAXRGqyRERvbaWKbtHVxGfaZ6rg", "maker": "7wiEWKeG7sFUNh1TgujwCa9cmJtSSE4mNLDde7knjoeE", "base_amount": 1701194.526509, "quote_amount": 2.942105783, "buy_cost_usd": 0, "token_amount": 1701194.526509, "amount_usd": 260.72941448946, "price": 0.000001729435251, "price_usd": 0.00015326255194362, "timestamp": 1778907856, "side": "buy", "is_open_or_close": 0, "base_address": "DkaY3z9hYutckCNoLCy8kfJvrDEDwjojQ9zL1s4Fpump", "balance": 0, "base_token": {"symbol": "F.03", "logo": "https://gmgn.ai/external-res/c91e2e6f1e1f9a3f17905598a42959e0_v2.webp", "total_supply": "940918890", "launchpad": "pump"}, "maker_info": {"avatar": "", "name": "", "tags": ["bullx", "padre", "smart_degen", "axiom"], "twitter_username": "", "twitter_name": ""}},
    {"transaction_hash": "4RTULAPkBSh1D1YPfJtxCniYtpHq16TxJjvzXLhNBFty4zxMYD8Z643BBc9XYW3xStcAiBLQPFrH2BSzpf6zVkbz", "maker": "7wiEWKeG7sFUNh1TgujwCa9cmJtSSE4mNLDde7knjoeE", "base_amount": 1738516.75977, "quote_amount": 2.942105783, "buy_cost_usd": 0, "token_amount": 1738516.75977, "amount_usd": 260.72941448946, "price": 0.0000016923079783, "price_usd": 0.000149972333036946, "timestamp": 1778907855, "side": "buy", "is_open_or_close": 1, "base_address": "DkaY3z9hYutckCNoLCy8kfJvrDEDwjojQ9zL1s4Fpump", "balance": 0, "base_token": {"symbol": "F.03", "logo": "https://gmgn.ai/external-res/c91e2e6f1e1f9a3f17905598a42959e0_v2.webp", "total_supply": "940918890", "launchpad": "pump"}, "maker_info": {"avatar": "", "name": "", "tags": ["bullx", "padre", "smart_degen", "axiom"], "twitter_username": "", "twitter_name": ""}},
    {"transaction_hash": "zQeYq2NvsDiryimByegujeKGNueSPuqg73krXpffn6mdM8TjwVDuRSrLMc7kni7aNBos2nWxNiGiB3uQu6qWadQ", "maker": "5kTMRBxmE9TmBjwehaZt1eF3wqx8Qv2GNyjKfdajqtBN", "base_amount": 7055728.000613, "quote_amount": 0.488888888, "buy_cost_usd": 0, "token_amount": 7055728.000613, "amount_usd": 43.33022214344, "price": 6.92896449e-8, "price_usd": 0.000006141141227487, "timestamp": 1778907843, "side": "buy", "is_open_or_close": 1, "base_address": "3S8sQAToTH1NFELwHzNmnYrwWsumpVaT3ri5bZNLpump", "balance": 0, "base_token": {"symbol": "Rose", "logo": "https://gmgn.ai/external-res/5a052a2041e1a436cf2da360aa85dece_v2.webp", "total_supply": "981875193", "launchpad": "pump"}, "maker_info": {"avatar": "", "name": "", "tags": ["smart_degen", "axiom"], "twitter_username": "", "twitter_name": ""}},
    {"transaction_hash": "3uKf2TGtxTfmaprXWVJ6KULtyApzp2BP3cak9txKBGGWEoefkKgva7wWkKqPrwnMKs42fJxYQRnishpq3MtCkqNy", "maker": "GoonY5hPo63xAPCwkyWuFmQ57HWq8wj5Bevj2D222U4u", "base_amount": 1520051.701329, "quote_amount": 1.960434782, "buy_cost_usd": 0, "token_amount": 1520051.701329, "amount_usd": 173.71412603302, "price": 0.0000012897158566, "price_usd": 0.000114281722053326, "timestamp": 1778907811, "side": "buy", "is_open_or_close": 1, "base_address": "DkaY3z9hYutckCNoLCy8kfJvrDEDwjojQ9zL1s4Fpump", "balance": 0, "base_token": {"symbol": "F.03", "logo": "https://gmgn.ai/external-res/c91e2e6f1e1f9a3f17905598a42959e0_v2.webp", "total_supply": "940918890", "launchpad": "pump"}, "maker_info": {"avatar": "", "name": "", "tags": ["smart_degen", "axiom"], "twitter_username": "", "twitter_name": ""}},
    {"transaction_hash": "5V8R2gbipXYMp6eHThouCM9eaEFe3bTvXQ2FmSbzgrcpfZywJjqt9aRZJyV8MbTCWyDTT1Rn9pX7vH9aYazSzEno", "maker": "2rnmRXibwTUYgVRGFuwrvp6oYcUcttL7E7XT3LYG7D4o", "base_amount": 20287547.477619, "quote_amount": 1.193685962, "buy_cost_usd": 88.2271604056, "token_amount": 20287547.477619, "amount_usd": 105.77251309282, "price": 5.8838357e-8, "price_usd": 0.00000521366681377, "timestamp": 1778907812, "side": "sell", "is_open_or_close": 1, "base_address": "2pKvEuWn7BF1wRUeG6QH6Bt4zrCvdJ6WFPtYoNMZpump", "balance": 0, "base_token": {"symbol": "Pinocchio", "logo": "https://gmgn.ai/external-res/92e648b10590f6a46ba00edeec1a3bf3_v2.webp", "total_supply": "999999926", "launchpad": "pump"}, "maker_info": {"avatar": "", "name": "", "tags": ["smart_degen", "gmgn"], "twitter_username": "", "twitter_name": ""}},
    {"transaction_hash": "34j8qzBTFFC5AFkoA1QTZuCCAymhqyvqcBfB3DZ1WCnocsfN2bZQXRNNZN9yT6hYAFxGkQd9zdJtuYhEABNGkkn7", "maker": "GoonY5hPo63xAPCwkyWuFmQ57HWq8wj5Bevj2D222U4u", "base_amount": 2120935.587538, "quote_amount": 3.153852162, "buy_cost_usd": 211.18175954324627, "token_amount": 2120935.587538, "amount_usd": 279.21053190186, "price": 0.0000014870098746, "price_usd": 0.000131644984198338, "timestamp": 1778907698, "side": "sell", "is_open_or_close": 1, "base_address": "DkaY3z9hYutckCNoLCy8kfJvrDEDwjojQ9zL1s4Fpump", "balance": 0, "base_token": {"symbol": "F.03", "logo": "https://gmgn.ai/external-res/c91e2e6f1e1f9a3f17905598a42959e0_v2.webp", "total_supply": "940918890", "launchpad": "pump"}, "maker_info": {"avatar": "", "name": "", "tags": ["smart_degen", "axiom"], "twitter_username": "", "twitter_name": ""}},
    {"transaction_hash": "45qeLssYtdnghnRxPR592kawDu2EisxqZe8AM56XNV3hCHBizyeHhZGi7hFYQj1jfDiM13GfUZyTd2SXq2sQzb7B", "maker": "5kTMRBxmE9TmBjwehaZt1eF3wqx8Qv2GNyjKfdajqtBN", "base_amount": 14531199.78136, "quote_amount": 0.684444444, "buy_cost_usd": 0, "token_amount": 14531199.78136, "amount_usd": 60.65546662728, "price": 4.71017159e-8, "price_usd": 0.000004174154063058, "timestamp": 1778907902, "side": "buy", "is_open_or_close": 0, "base_address": "3S8sQAToTH1NFELwHzNmnYrwWsumpVaT3ri5bZNLpump", "balance": 0, "base_token": {"symbol": "Rose", "logo": "https://gmgn.ai/external-res/5a052a2041e1a436cf2da360aa85dece_v2.webp", "total_supply": "981875193", "launchpad": "pump"}, "maker_info": {"avatar": "", "name": "", "tags": ["smart_degen", "axiom"], "twitter_username": "", "twitter_name": ""}},
    {"transaction_hash": "66JKzv3pqR1kwVKb1gK67HA1CubHJaXTPsaMxEaBo9VRkhqSpxj7KdJsVP4KjC9wHqFshZJifY5JKYVftm4RYbxB", "maker": "5kTMRBxmE9TmBjwehaZt1eF3wqx8Qv2GNyjKfdajqtBN", "base_amount": 14948890.834797, "quote_amount": 0.684444444, "buy_cost_usd": 0, "token_amount": 14948890.834797, "amount_usd": 60.66231107172, "price": 4.5785634e-8, "price_usd": 0.00000405798074142, "timestamp": 1778907897, "side": "buy", "is_open_or_close": 1, "base_address": "3S8sQAToTH1NFELwHzNmnYrwWsumpVaT3ri5bZNLpump", "balance": 0, "base_token": {"symbol": "Rose", "logo": "https://gmgn.ai/external-res/5a052a2041e1a436cf2da360aa85dece_v2.webp", "total_supply": "981875193", "launchpad": "pump"}, "maker_info": {"avatar": "", "name": "", "tags": ["smart_degen", "axiom"], "twitter_username": "", "twitter_name": ""}},
    {"transaction_hash": "3LivcqGVWsg3mBpJrud6n5UiZprHJSgiZ1aFz12N9vHybuFWF1FMxZhCDKBVdDcagHr1NV5nMZKPfFiJvBEQLES6", "maker": "5kTMRBxmE9TmBjwehaZt1eF3wqx8Qv2GNyjKfdajqtBN", "base_amount": 11048776.086463, "quote_amount": 0.684444444, "buy_cost_usd": 0, "token_amount": 11048776.086463, "amount_usd": 60.64862218284, "price": 6.19475351e-8, "price_usd": 0.000005489171085211, "timestamp": 1778907881, "side": "buy", "is_open_or_close": 0, "base_address": "3S8sQAToTH1NFELwHzNmnYrwWsumpVaT3ri5bZNLpump", "balance": 0, "base_token": {"symbol": "Rose", "logo": "https://gmgn.ai/external-res/5a052a2041e1a436cf2da360aa85dece_v2.webp", "total_supply": "981875193", "launchpad": "pump"}, "maker_info": {"avatar": "", "name": "", "tags": ["smart_degen", "axiom"], "twitter_username": "", "twitter_name": ""}},
  ]
}

# Get unique BUY transactions (dedup by token+wallet, keep most recent)
buys = {}
for tx in data["list"]:
    if tx["side"] != "buy":
        continue
    key = f"{tx['maker']}:{tx['base_address']}"
    if key not in buys or tx["timestamp"] > buys[key]["timestamp"]:
        buys[key] = tx

# Get unique token addresses
unique_tokens = list(set(tx["base_address"] for tx in buys.values()))
print(f"Unique tokens to analyze: {len(unique_tokens)}")
print(f"Unique buy transactions: {len(buys)}")

# Fetch token info for each
token_data = {}
for addr in unique_tokens:
    try:
        result = subprocess.run(
            ["gmgn-cli", "token", "info", "--chain", "sol", "--address", addr, "--raw"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            token_data[addr] = json.loads(result.stdout)
        else:
            print(f"Error fetching {addr}: {result.stderr}")
        time.sleep(0.5)  # Rate limit
    except Exception as e:
        print(f"Exception fetching {addr}: {e}")

print(f"\nSuccessfully fetched: {len(token_data)} tokens")

# Now analyze each buy
passed = []
failed = {"too_old": 0, "low_volume": 0, "volume_collapsed": 0, "dumping": 0, "distribution": 0, "low_holders": 0, "high_bot": 0}

for key, tx in buys.items():
    addr = tx["base_address"]
    symbol = tx["base_token"]["symbol"]
    wallet = tx["maker"]
    amount_usd = tx["amount_usd"]
    is_full = tx["is_open_or_close"]
    
    # Check if wallet is in our tiers
    tier = None
    if wallet in TIER1:
        tier = "T1"
    elif wallet in TIER2:
        tier = "T2"
    
    if addr not in token_data:
        continue
    
    info = token_data[addr]
    
    # Extract data
    try:
        creation_time = info.get("creation_timestamp", 0)
        age_min = (CURRENT_TIME - creation_time) / 60 if creation_time else 999
        
        # Volume data
        vol_5m = info.get("volume_5m", 0) or info.get("swap_5m", 0) or 0
        vol_1h = info.get("volume_1h", 0) or info.get("swap_1h", 0) or 0
        vol_trend = (vol_5m / (vol_1h / 12)) if vol_1h > 0 else 0
        
        # Price data
        price = info.get("price", 0) or tx.get("price_usd", 0)
        price_1h_high = info.get("price_1h_high", 0) or info.get("high_1h", 0) or price
        price_vs_high = (price / price_1h_high * 100) if price_1h_high > 0 else 100
        
        # Buy/sell ratio
        buys_1h = info.get("buys_1h", 0) or 0
        sells_1h = info.get("sells_1h", 0) or 0
        buy_ratio = (buys_1h / (buys_1h + sells_1h)) if (buys_1h + sells_1h) > 0 else 0.5
        
        # Holders
        holders = info.get("holder_count", 0) or info.get("holders", 0) or 0
        
        # Bot rate
        bot_rate = info.get("bot_degen_rate", 0) or info.get("bot_rate", 0) or 0
        
        # Market cap
        mcap = info.get("market_cap", 0) or 0
        
        # Apply filters
        filters_passed = 0
        filter_results = {}
        
        # 1. Age < 30 min
        if age_min < 30:
            filters_passed += 1
            filter_results["age"] = True
        else:
            filter_results["age"] = False
            failed["too_old"] += 1
            
        # 2. Volume 5m > $5K
        if vol_5m > 5000:
            filters_passed += 1
            filter_results["volume"] = True
        else:
            filter_results["volume"] = False
            failed["low_volume"] += 1
            
        # 3. Volume trend > 20% of 1h average
        if vol_trend > 0.20:
            filters_passed += 1
            filter_results["vol_trend"] = True
        else:
            filter_results["vol_trend"] = False
            failed["volume_collapsed"] += 1
            
        # 4. Price vs 1h high > 70%
        if price_vs_high > 70:
            filters_passed += 1
            filter_results["price"] = True
        else:
            filter_results["price"] = False
            failed["dumping"] += 1
            
        # 5. Buy/Sell ratio > 0.6
        if buy_ratio > 0.6:
            filters_passed += 1
            filter_results["ratio"] = True
        else:
            filter_results["ratio"] = False
            failed["distribution"] += 1
            
        # 6. Holders > 100
        if holders > 100:
            filters_passed += 1
            filter_results["holders"] = True
        else:
            filter_results["holders"] = False
            failed["low_holders"] += 1
            
        # 7. Bot rate < 40%
        if bot_rate < 40:
            filters_passed += 1
            filter_results["bot"] = True
        else:
            filter_results["bot"] = False
            failed["high_bot"] += 1
        
        # Check if ALL passed
        all_passed = all(filter_results.values())
        
        # Check for cluster signal (multiple wallets buying same token)
        cluster = sum(1 for k, v in buys.items() if v["base_address"] == addr) > 1
        
        result = {
            "wallet": wallet,
            "tier": tier,
            "symbol": symbol,
            "address": addr,
            "amount_usd": amount_usd,
            "is_full": is_full,
            "mcap": mcap,
            "age_min": age_min,
            "vol_5m": vol_5m,
            "vol_trend": vol_trend,
            "price_vs_high": price_vs_high,
            "buy_ratio": buy_ratio,
            "holders": holders,
            "bot_rate": bot_rate,
            "filters_passed": filters_passed,
            "all_passed": all_passed,
            "cluster": cluster,
            "filter_results": filter_results,
        }
        
        if all_passed:
            passed.append(result)
        
    except Exception as e:
        print(f"Error analyzing {symbol}: {e}")

# Print report
print("\n" + "="*80)
print("SMART MONEY TRACKER REPORT")
print(f"Time: {datetime.utcfromtimestamp(CURRENT_TIME).strftime('%Y-%m-%d %H:%M:%S')} UTC")
print("="*80)

if passed:
    print(f"\n🔥 HIGH-CONVICTION SIGNALS: {len(passed)} tokens passed ALL filters")
    print("-"*80)
    
    for p in passed:
        wallet_name = TIER1.get(p["wallet"], TIER2.get(p["wallet"], p["wallet"][:8] + "..."))
        full_text = "FULL" if p["is_full"] else "PARTIAL"
        
        print(f"\n🔥 HIGH-CONVICTION SIGNAL ({p['filters_passed']}/7 filters passed)")
        print(f"[{datetime.utcfromtimestamp(CURRENT_TIME).strftime('%H:%M')}] {wallet_name} — BUY ${p['symbol']} ${p['amount_usd']:.2f} [{full_text}]")
        print(f"📍 {p['address']}")
        print(f"💰 MCAP: ${p['mcap']:,.0f} | Price: ${p.get('price', 0):.8f} | vs 1h High: {p['price_vs_high']:.1f}%")
        print(f"⏱️ Age: {p['age_min']:.1f} min | Vol 5m: ${p['vol_5m']:,.0f} | Vol Trend: {p['vol_trend']*100:.0f}%")
        print(f"📊 Buy Ratio: {p['buy_ratio']*100:.1f}% | Holders: {p['holders']} | Bot Rate: {p['bot_rate']:.1f}%")
        print(f"🔗 DexScreener: https://dexscreener.com/solana/{p['address']}")
        print(f"💵 Buy: /buy {p['address']} 0.1")
        print(f"\n⚡ CONVICTION INDICATORS:")
        print(f"• Multiple wallets: {'YES' if p['cluster'] else 'NO'}")
        print(f"• Large amount: {'YES' if p['amount_usd'] > 500 else 'NO'}")
        print(f"• Full position: {'YES' if p['is_full'] else 'NO'}")
        print(f"• Fresh + high volume: {'YES' if p['age_min'] < 15 and p['vol_5m'] > 10000 else 'NO'}")
else:
    print("\n❌ NO HIGH-CONVICTION SIGNALS found")

# Print filter summary
total_skipped = sum(failed.values())
print(f"\n📊 FILTERED OUT: {total_skipped} low-conviction buys skipped")
print(f"• Too old (>30min): {failed['too_old']}")
print(f"• Low volume (<$5K 5m): {failed['low_volume']}")
print(f"• Volume collapsed (<20% of 1h avg): {failed['volume_collapsed']}")
print(f"• Dumping (<70% of 1h high): {failed['dumping']}")
print(f"• Distribution (buy ratio <0.6): {failed['distribution']}")
print(f"• Low holders (<100): {failed['low_holders']}")
print(f"• High bot rate (>40%): {failed['high_bot']}")

print("\n" + "="*80)
