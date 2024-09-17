#!/usr/bin/python

import csv
import requests
import json
import time


verisUrl = "https://api.com/"
token = "$token"


def getTradeById(id):
	headers = {             
		'Accept': 'application/json',
		'Content-Type': 'application/json',
		'Authorization': f'Bearer {token}'
	}
	url = f'{verisUrl}/api/v3/transactional/trade/id/{id}'
	response = requests.get(url, headers=headers)

	return response.json()


def getPairById(pairId):
	headers = {
		'Accept': 'application/json',
		'Content-Type': 'application/json',
		'Authorization': f'Bearer {token}'
	}               
	url = f'{verisUrl}/api/v3/transactional/trade/paired-data/{pairId}'
	response = requests.get(url, headers=headers)

	return response.json()


def getFilteredTrade(id):
	headers = {
		'Accept': 'application/json',
		'Content-Type': 'application/json',
		'Authorization': f'Bearer {token}'
	}
	url = f'{verisUrl}/api/v3/transactional/trades?pageOffset=0&pageLimit=5&canceled=false&tradeRef={id}'
	response = requests.get(url, headers=headers)

	return response.json()



def getMessageReceipt(trackingId):
	headers = {
		'Accept': '*/*',
		'Content-Type': 'application/json',
		'Authorization': f'Bearer {token}'
	}       
	url = f'{verisUrl}/api/v3/metadata/message/{trackingId}'
	response = requests.get(url, headers=headers)

	if(response.status_code != 200):
		print(f"[-] Did not receive 200 response from /api/v3/metadata/message/")

	return response.json()





if __name__ == '__main__':

	rows = []
	# Open the CSV file in read mode
	output = "partyA,partyB,pairingStatus,primaryMatchingStatus,SecondaryMatchingStatus\n"
	with open('trades.csv', 'r') as csvfile:
		csv_string = csvfile.read()
		rows = csv_string.split("\n")

	for line in rows:

		if(len(line) < 2):
			continue

		print(f"[+] Looking for {line} ...")
		result = getFilteredTrade(line)
		t = str(result)
		if(len(t) < 5):
			print(f"[-] No results returned")
			continue
		try:
			contractRef = result[0]['contractRef']
			primaryMatchingStatus = result[0]['matchingStatus']['primaryMatchingStatus']
			secondaryMatchingStatus = result[0]['matchingStatus']['secondaryMatchingStatus']
			pairingStatus = result[0]['pairingStatus']
			id = result[0]['id']
		except (AttributeError, KeyError):
			print(f"[-] Error extracting trade data")

		pairType = list(result[0]['pairingStatus'].keys())[0]
		if("pairId" in t):
			pairId = result[0]['pairingStatus'][pairType]['pairId']
			result = getPairById(pairId)
			try:
				partyBTradeId = result['partyBTradeId']
				partyATradeId = result['partyATradeId']
				primaryMatchingStatus = result['primaryMatchingStatus']
				secondaryMatchingStatus = result['secondaryMatchingStatus']
				if(id in partyATradeId):
					result = getTradeById(partyBTradeId)
				else:
					result = getTradeById(partyATradeId)

				partyBTradeRef = result['tradeRef']
				print(f"[+] Trade {line} is {pairType} with {partyBTradeRef} with primary matching status {primaryMatchingStatus}")
				output = output + line + "," + partyBTradeRef + "," + pairType + "," + primaryMatchingStatus + "," + secondaryMatchingStatus + "\n"
			except (AttributeError, KeyError):
				print(f"[-] Error looking for paired counterparty")

		else:
			print(f"[-] Trade {line} is {pairType}")
			output = output + line + ",," + pairType + ",,\n"


		print("")


	print(f"Hope you had fun.  CSV is\n{output}")




