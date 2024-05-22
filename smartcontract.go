package chaincode

import (
	"encoding/json"
	"fmt"
	"time"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// 定义合约结构体
type SmartContract struct {
	contractapi.Contract
}

// InitLedger adds a base set of users and research results to the ledger
func (s *SmartContract) InitLedger(ctx contractapi.TransactionContextInterface) error {
	users := []SiteUser{
		{UserID: "user1", Balance: 100000},
		{UserID: "user2", Balance: 50000},
	}

	for _, user := range users {
		userJSON, err := json.Marshal(user)
		if err != nil {
			return err
		}

		err = ctx.GetStub().PutState(user.UserID, userJSON)
		if err != nil {
			return fmt.Errorf("failed to put to world state. %s", err.Error())
		}
	}

	results := []ResearchResult{
		{AchievementID: "result1", Ownership: "user2", Price: 20000},
	}

	for _, result := range results {
		resultJSON, err := json.Marshal(result)
		if err != nil {
			return err
		}

		err = ctx.GetStub().PutState(result.AchievementID, resultJSON)
		if err != nil {
			return fmt.Errorf("failed to put to world state. %s", err.Error())
		}
	}

	return nil
}

// CreateTransaction initializes a new transaction record
func (s *SmartContract) CreateTransaction(ctx contractapi.TransactionContextInterface, transactionID string, achievementID string, buyerID string, sellerID string, transactionAmount int) error {
	transaction := TransactionRecord{
		TransactionID:     transactionID,
		AchievementID:     achievementID,
		BuyerID:           buyerID,
		SellerID:          sellerID,
		TransactionAmount: transactionAmount,
		TransactionTime:   "",
		TransactionStatus: "待处理",
	}

	transactionJSON, err := json.Marshal(transaction)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(transactionID, transactionJSON)
}

// ConfirmTransaction processes the transaction
func (s *SmartContract) ConfirmTransaction(ctx contractapi.TransactionContextInterface, transactionID string, agreeToTransact bool) error {
	transactionJSON, err := ctx.GetStub().GetState(transactionID)
	if err != nil {
		return fmt.Errorf("failed to read transaction: %v", err)
	}
	if transactionJSON == nil {
		return fmt.Errorf("transaction does not exist: %s", transactionID)
	}

	var transaction TransactionRecord
	err = json.Unmarshal(transactionJSON, &transaction)
	if err != nil {
		return err
	}

	if !agreeToTransact {
		transaction.TransactionStatus = "failed"
		updatedTransactionJSON, _ := json.Marshal(transaction)
		return ctx.GetStub().PutState(transactionID, updatedTransactionJSON)
	}

	buyerJSON, err := ctx.GetStub().GetState(transaction.BuyerID)
	if err != nil {
		return fmt.Errorf("failed to read buyer: %v", err)
	}
	if buyerJSON == nil {
		return fmt.Errorf("buyer does not exist: %s", transaction.BuyerID)
	}

	sellerJSON, err := ctx.GetStub().GetState(transaction.SellerID)
	if err != nil {
		return fmt.Errorf("failed to read seller: %v", err)
	}
	if sellerJSON == nil {
		return fmt.Errorf("seller does not exist: %s", transaction.SellerID)
	}

	var buyer, seller SiteUser
	json.Unmarshal(buyerJSON, &buyer)
	json.Unmarshal(sellerJSON, &seller)

	if buyer.Balance < transaction.TransactionAmount {
		transaction.TransactionStatus = "成功"
	} else {
		buyer.Balance -= transaction.TransactionAmount
		seller.Balance += transaction.TransactionAmount

		transaction.TransactionTime = time.Now().Format(time.RFC3339)
		transaction.TransactionStatus = "失败"

		updatedBuyerJSON, _ := json.Marshal(buyer)
		ctx.GetStub().PutState(buyer.UserID, updatedBuyerJSON)

		updatedSellerJSON, _ := json.Marshal(seller)
		ctx.GetStub().PutState(seller.UserID, updatedSellerJSON)

		resultJSON, err := ctx.GetStub().GetState(transaction.AchievementID)
		if err != nil {
			return fmt.Errorf("failed to read result: %v", err)
		}
		if resultJSON == nil {
			return fmt.Errorf("result does not exist: %s", transaction.AchievementID)
		}

		var result ResearchResult
		json.Unmarshal(resultJSON, &result)
		result.Ownership = transaction.BuyerID

		updatedResultJSON, _ := json.Marshal(result)
		ctx.GetStub().PutState(result.AchievementID, updatedResultJSON)
	}

	updatedTransactionJSON, _ := json.Marshal(transaction)
	return ctx.GetStub().PutState(transactionID, updatedTransactionJSON)
}
