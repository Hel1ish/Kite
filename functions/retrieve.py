from pymongo import MongoClient
client = MongoClient('mongodb+srv://Xynx_Dev:rabMue6xhQJH7gNR@kite-cluster.ie2xvdk.mongodb.net/?retryWrites=true&w=majority')
mong = client.get_database('Data')
database = mong.UserData

class GET:
    def data(self, userid):
        user = database.find_one({"_id": userid})
        username=user["name"]
        email=user["email"]
        phone=user["phone#"]
        cbal=user["tcrypto"]
        wbal=user["wbalance"]
        school=user["school"]
        schoolid=user["schoolID"]
        return [username, email, phone, cbal, wbal, user, school, schoolid]
    def transaction(self, amount, senderid, receiverid):
        sender = database.find_one({"_id": senderid})
        receiver = database.find_one({"_id": receiverid})
        if int(amount) <= int(sender["wbalance"]):
          balanceleft = int(sender["wbalance"]) - int(amount)
          update = { "$set": { 'wbalance': balanceleft } }
          database.update_one({"_id": senderid }, update) 
          newbalance = int(receiver["wbalance"]) + int(amount)
          update = { "$set": {'wbalance': newbalance } }
          database.update_one({"_id": receiverid }, update)
          return "Transaction completed"
        elif int(amount) >= int(sender["wbalance"]):
          return "This transaction has failed. Insufficient funds"
    def addbal(self, amount, user):
        add = database.find_one({"_id": user})
        print(amount)
        print(add["wbalance"])
        newbal = add["wbalance"] + int(amount)
        update = { "$set": { 'wbalance': int(newbal) } }
        database.update_one({"_id": user }, update)
        return f"${amount} has been added to your wallet" 