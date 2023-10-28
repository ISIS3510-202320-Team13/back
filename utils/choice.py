class Choice:
    compared = {}
    choosed = {}
    choosed_id = ""
    rate = -1
    price = 0

    def get_choosed(self):
        choice = self.compared.pop(self.choosed_id)

        choice['uid'] = self.choosed_id
        
        if self.price == choice["price"]:
            choice["price_match"] = True
        else:
            choice["price_match"] = False
        
        self.compared['choice'] = choice
        return self.compared
    
    def compare_to_choosed(self, docdic:dict, dist:int, uid:str):

        t_price, t_rate = calculate_rate(docdic)        

        if self.choosed == {}:
            self.choosed = docdic
            self.choosed_id = uid
            self.rate = t_rate
            self.price = t_price
            
            
        else:
            
            if dist <= 500:
                if (self.rate == -1) or (self.rate < (t_rate)):
                    self.rate = t_rate
                    
                    self.choosed_id = uid
                    self.choosed = docdic
                
                if self.price > t_price:
                    self.price = t_price

                docdic["distance"] = round(dist, 2)
                self.compared[uid] = docdic

        return docdic
        
def calculate_rate(docdic:dict):
    t_price = docdic["price"]
    t_rate = docdic["rating"]+((-1*t_price)/100)
    return t_price, t_rate