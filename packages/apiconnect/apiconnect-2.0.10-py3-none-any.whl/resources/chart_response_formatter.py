class ChartResponseFormatter :
    def __init__(self, response) -> None:
        self.__response_dict = response
        # self.__plot_points = self.__response_dict['data']['pltPnts']
        # self.__ltt = self.__plot_points['ltt']
        # self.__open = self.__plot_points['open']
        # self.__high = self.__plot_points['high']
        # self.__low = self.__plot_points['low']
        # self.__close = self.__plot_points['close']
        # self.__vol = self.__plot_points['vol']
        # self.__nextTillDate = self.__plot_points['ltt'][0]

        data = self.__response_dict.get("data")
        if not data or "pltPnts" not in data:
            self.LOGGER.error(f"Invalid success response format: {self.__response_dict}")
            raise Exception("Chart API returned invalid data format")

        self.__plot_points = data["pltPnts"]

        self.__ltt   = self.__plot_points.get("ltt", [])
        self.__open  = self.__plot_points.get("open", [])
        self.__high  = self.__plot_points.get("high", [])
        self.__low   = self.__plot_points.get("low", [])
        self.__close = self.__plot_points.get("close", [])
        self.__vol   = self.__plot_points.get("vol", [])

        if self.__ltt:
            self.__nextTillDate = self.__ltt[0]
        else:
            self.__nextTillDate = None
            self.LOGGER.warning("No ltt data found in chart response")


    def getOHCLResponse(self) :

        # a list of mapped elements, index wise from all 5 lists
        ltt_o_h_c_l_vol = [list(x) for x in zip(self.__ltt, self.__open, self.__high, self.__low, self.__close, self.__vol)]

        formatted_response_dict = { 'msgID' : self.__response_dict['msgID'],
                                    'srvTm' : self.__response_dict['srvTm'],
                                    'data' : ltt_o_h_c_l_vol,
                                    'nextTillDate' : self.__nextTillDate
                                    }

        return(formatted_response_dict)
    
    def getCustomPeriodOHCLResponse(self) :

        # a list of mapped elements, index wise from all 5 lists
        ltt_o_h_c_l_vol = [list(x) for x in zip(self.__ltt, self.__open, self.__high, self.__low, self.__close, self.__vol)]

        formatted_response_dict = { 'msgID' : self.__response_dict['msgID'],
                                    'srvTm' : self.__response_dict['srvTm'],
                                    'data' : ltt_o_h_c_l_vol
                                  }

        return(formatted_response_dict)