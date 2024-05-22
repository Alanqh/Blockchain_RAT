package chaincode

type SiteUser struct {
	UserID  string `json:"userID"`
	Balance int    `json:"balance"`
}

// ResearchResult describes a research result
type ResearchResult struct {
	AchievementID string `json:"achievementID"`
	Ownership     string `json:"ownership"`
	Price         int    `json:"price"`
}

// TransactionRecord describes a transaction
type TransactionRecord struct {
	TransactionID     string `json:"transactionID"`
	AchievementID     string `json:"achievementID"`
	BuyerID           string `json:"buyerID"`
	SellerID          string `json:"sellerID"`
	TransactionAmount int    `json:"transactionAmount"`
	TransactionTime   string `json:"transactionTime"`
	TransactionStatus string `json:"transactionStatus"`
}