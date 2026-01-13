from utility.library import *

logger = logging.getLogger(__name__)


class Exchange(enum.Enum):
    NSE = "NSE"
    BSE = "BSE"
    NFO = "NFO"
    BFO = "BFO"
    CDS = "CDS"
    BCD = "BCD"
    NCO = "NCO"
    BCO = "BCO"
    MCX = "MCX"
    INDICES = "INDICES"
    NCDEX = "NCDEX"
    NSE_FO = "nse_fo"
    BSE_FO = "bse_fo"
    MCX_FO = "mcx_fo"


@dataclass(frozen=False)
class Instrument:
    exchange: Optional[Any]
    token: Optional[Any]
    symbol: Optional[Any]
    trading_symbol: Optional[Any]
    expiry: Optional[Any]
    lot_size: Optional[Any]


class Websocket_API:
    ENC = None
    ws = None
    subscriptions = None
    __subscribe_callback = None
    __subscribers = None
    script_subscription_instrument = []
    ws_connection = False
    # response = requests.get(base_url);
    # Getscrip URI
    __ws_thread = None
    __stop_event = None
    market_depth = None

    def __init__(
            self,
            user_id: Union[str, int],
            auth_code: str,
            secret_key: str,
            base_url: str = None,
            session_id: str = None,
            __on_error: str = None,
            __on_disconnect: str = None,
            __on_open: str = None,
    ):
        self._user_id = user_id.upper()
        self._auth_code = auth_code
        self._secret_key = secret_key
        self._session_id = session_id
        self.__on_error = None
        self.__on_disconnect = None
        self.__on_open = None
        self.websocket_url = 'wss://ws1.aliceblueonline.com/NorenWS/'
        self._base_url = base_url or ServiceProps.BASE_URL
        self._endpoints = {
            # API User Authorization Part
            "getSession": ServiceProps.GET_VENDOR_SESSION,

            # User & Portfolio Management Part
            "getProfile": ServiceProps.GET_PROFILE,
            "getFunds": ServiceProps.GET_FUNDS,
            "getPositions": ServiceProps.GET_POSITIONS,
            "getHoldings": ServiceProps.GET_HOLDINGS,

            # Position Conversion & Margin Management Part
            "posConversion": ServiceProps.POSITION_CONVERSION,
            "positionSqrOff": ServiceProps.POSITION_SQR_OFF,
            "SingleOrdMargin": ServiceProps.SINGLE_ORDER_MARGIN,

            # Order & Trade Management Part
            "ordExecute": ServiceProps.ORDER_EXECUTE,
            "ordModify": ServiceProps.ORDER_MODIFY,
            "ordCancel": ServiceProps.ORDER_CANCEL,
            "ordExitBracket": ServiceProps.EXIT_BRACKET_ORDER,

            # GTT Order & Trade Management Part
            "ordGTT_Execute": ServiceProps.GTT_ORDER_EXECUTE,
            "ordGTT_Modify": ServiceProps.GTT_ORDER_MODIFY,
            "ordGTT_Cancel": ServiceProps.GTT_ORDER_CANCEL,

            # Order & Trade History Retrieval Part
            "getOrderbook": ServiceProps.GET_ORDER_BOOK,
            "getTradebook": ServiceProps.GET_TRADE_BOOK,
            "getOrdHistory": ServiceProps.GET_ORDER_HISTORY,

            # GTT Orders Retrieval Part
            "getGTTOrderbook": ServiceProps.GET_GTT_ORDER_BOOK,

            # Chart & Historical Data Part
            "getChartHistory": ServiceProps.GET_CHART_HISTORY,

            # GetUnderlying for Optionchain
            "getUnderlying": ServiceProps.GET_UNDERLYING,
            "getUnderlyingExpiry": ServiceProps.GET_UNDERLYING_EXPIRY,
            "getOptionChain": ServiceProps.GET_OPTION_CHAIN,
            "getBasketMargin": ServiceProps.GET_BASKETMARGIN,
            "getHistoricalData": ServiceProps.GET_HISTORICAL_DATA,
            "getWStoken": ServiceProps.GET_WEBSOCKET_TOKEN,
            "getWSSession": ServiceProps.GET_WSSSESSION,
            "getInvalidSession": ServiceProps.GET_INVALIDSESSION_WS,
            "getCreateSession": ServiceProps.GET_CREATESESSION_WS
        }

    @staticmethod
    def _errorResponse(message: str, encKey=None):
        return {'stat': 'Not_ok', 'emsg': message, 'encKey': encKey}

    def _init_session(self):
        return RequestHandler(session_token=self.sessionAuthorization())

    def sessionAuthorization(self):
        # Return the Bearer token if _session_id is available, else return empty string
        if self._session_id:
            return f"Bearer {self._session_id}"
        else:
            return ""

    def get_instrument(self, exchange: Union[str, Exchange], symbol: Union[str] = None, token: Union[str, int] = None):
        """
        Get instrument details using symbol or token for a given exchange.

        Parameters:
            exchange (str): Exchange name (e.g., 'NSE', 'BSE', 'NFO', 'INDICES').
            symbol (str, optional): Symbol or trading symbol of the instrument.
            token (str or int, optional): Token of the instrument.

        Returns:
            Instrument: Instrument details if found.

        Error:
            Returns error response if symbol/token not found or contract file is missing.
        """

        # Handle Both Enum and String
        exchange = getattr(exchange, 'value', exchange)

        if not symbol and not token:
            return self._errorResponse(message="Either symbol or token must be provided")

        try:
            contract = contract_read(exchange)
        except OSError as e:
            if e.errno == 2:
                self.get_contract_master(exchange)
                contract = contract_read(exchange)
            else:
                return self._errorResponse(message=str(e))

        if exchange == 'INDICES':
            filter_contract = contract[contract['token'] == token] if token else contract[
                contract['symbol'] == symbol.upper()]

            if filter_contract.empty:
                return self._errorResponse(message="The symbol is not available in this exchange")

            filter_contract = filter_contract.reset_index(drop=True)

            inst = Instrument(
                exchange=filter_contract.at[0, 'exch'],
                token=filter_contract.at[0, 'token'],
                symbol=filter_contract.at[0, 'symbol'],
                trading_symbol='',
                expiry='',
                lot_size=''
            )

            return inst

        else:
            filter_contract = contract[contract['Token'] == token] if token else contract[
                (contract['Symbol'] == symbol.upper()) | (contract['Trading Symbol'] == symbol.upper())]

            if filter_contract.empty:
                return self._errorResponse(message="The symbol is not available in this exchange")

            filter_contract = filter_contract.reset_index(drop=True)

            expiry = (
                filter_contract.at[0, 'Expiry Date']
                if 'Expiry Date' in filter_contract.columns
                else (
                    filter_contract.at[0, 'expiry_date']
                    if 'expiry_date' in filter_contract.columns
                    else ''
                )
            )

            inst = Instrument(
                exchange=filter_contract.at[0, 'Exch'],
                token=filter_contract.at[0, 'Token'],
                symbol=filter_contract.at[0, 'Symbol'],
                trading_symbol=filter_contract.at[0, 'Trading Symbol'],
                expiry=expiry,
                lot_size=filter_contract.at[0, 'Lot Size']
            )

            return inst

    # def _init_post(self, _endpoints_key, data=None, params=None, pathParameter=None):
    #     """Send a POST request to the specified endpoint key with optional path parameter."""
    #     # Construct the URL safely
    #     endpoint = self._endpoints.get(_endpoints_key, "")
    #     if not endpoint:
    #         return self._errorResponse(message=f"Invalid endpoint key: {_endpoints_key}")
    #
    #     url = self._base_url + endpoint
    #     # Append the path parameter if provided
    #     if pathParameter:
    #         # Ensure there's a slash between the endpoint and the path parameter
    #         if not url.endswith('/'):
    #             url += '/'
    #         url += str(pathParameter)  # Convert to string in case it's not
    #
    #     api = self._init_session()
    #     print(api)
    #     return api.request(url=url, method="POST", data=data, params=params)
    #
    # def get_session_id(self, check_sum=None, session_id=None):
    #     """
    #     Retrieves or generates a session ID (checksum) for user authentication.
    #
    #     Args:
    #         check_sum (str, optional): An existing checksum. If provided and valid, it will be used.
    #         session_id (str, optional): An existing session token. If provided and valid, it will be used.
    #
    #     Returns:
    #         dict: A dictionary containing the 'userSession' value used for API requests.
    #     """
    #
    #     if session_id and session_id.strip():
    #         self._session_id = session_id.strip()
    #         return {"userSession": self._session_id}
    #
    #     try:
    #         if not check_sum or not check_sum.strip():
    #             check_sum = generate_checksum(
    #                 user_id=self._user_id,
    #                 auth_Code=self._auth_code,
    #                 secret_key=self._secret_key
    #             )
    #         else:
    #             check_sum = check_sum.strip()
    #
    #         data = {'checkSum': check_sum}
    #         response = self._init_post(_endpoints_key="getSession", data=data)
    #         print(response)
    #
    #         self._session_id = None
    #
    #         if response and (response.get('status') == 'Ok' or response.get('stat') == 'Ok'):
    #             result = response.get('result')
    #             if response.get('status') == 'Ok' and isinstance(result, list) and len(result) > 0 and isinstance(
    #                     result[0], dict):
    #                 access_token = result[0].get('accessToken')
    #                 if access_token:
    #                     self._session_id = access_token
    #                     return {"userSession": self._session_id}
    #             elif response.get('stat') == 'Ok' and response.get('userSession'):
    #                 self._session_id = response.get('userSession')
    #                 return {"userSession": self._session_id}
    #             else:
    #                 # Handle cases where 'result' is missing or empty
    #                 return self._errorResponse(message="Session ID not found in response.")
    #         else:
    #             return self._errorResponse(message=response.get('message') or response.get('emsg'))
    #
    #
    #     except Exception as e:
    #         return self._errorResponse(message=f"Error generating session: {str(e)}")

    def invalid_sess(self, session_ID):

        url = 'https://a3.aliceblueonline.com/open-api/od/v1/profile/invalidateWsSess'

        headers = {
            'Authorization': 'Bearer ' + session_ID,
            'Content-Type': 'application/json'
        }
        payload = {
            "source": "API",
            "userId": self._user_id
        }
        data = json.dumps(payload)
        response = requests.request("POST", url, headers=headers, data=data)
        return response.json()

    def createSession(self, session_ID):
        url = 'https://a3.aliceblueonline.com/open-api/od/v1/profile/createWsSess'

        headers = {
            'Authorization': 'Bearer ' + session_ID,
            'Content-Type': 'application/json'
        }
        payload = {
            "source": "API",
            "userId": self._user_id
        }
        data = json.dumps(payload)
        response = requests.request("POST", url, headers=headers, data=data)
        return response.json()

    def __ws_run_forever(self):
        while self.__stop_event.is_set() is False:
            try:
                self.ws.run_forever(ping_interval=3, ping_payload='{"t":"h"}', sslopt={"cert_reqs": ssl.CERT_NONE})
            except Exception as e:
                logger.warning(f"websocket run forever ended in exception, {e}")
            sleep(1)

    def on_message(self, ws, message):
        self.__subscribe_callback(message)
        data = json.loads(message)

    def on_error(self, ws, error):
        if (
                type(
                    ws) is not websocket.WebSocketApp):  # This workaround is to solve the websocket_client's compatiblity issue of older versions. ie.0.40.0 which is used in upstox. Now this will work in both 0.40.0 & newer version of websocket_client
            error = ws
        if self.__on_error:
            self.__on_error(error)

    def on_close(self, *arguments, **keywords):
        self.ws_connection = False
        if self.__on_disconnect:
            self.__on_disconnect()

    def stop_websocket(self):
        self.ws_connection = False
        self.ws.close()
        self.__stop_event.set()

    def on_open(self, ws):
        def sha256_encryption(val):
            return hashlib.sha256(val.encode("utf-8")).hexdigest()

        raw = self._session_id.strip()
        first = sha256_encryption(raw)
        enc_val = sha256_encryption(first)

        initCon = {
            "susertoken": enc_val,
            "t": "c",
            "actid": self._user_id + "_API",
            "uid": self._user_id + "_API",
            "source": "API"
        }

        self.ws.send(json.dumps(initCon))
        self.ws_connection = True
        if self.__on_open:
            self.__on_open()

    def subscribe(self, instrument):
        scripts = ""
        for __instrument in instrument:
            scripts = scripts + __instrument.exchange + "|" + str(__instrument.token) + "#"
        self.subscriptions = scripts[:-1]
        if self.market_depth:
            t = "d"  # Subscribe Depth
        else:
            t = "t"  # Subsribe token
        data = {
            "k": self.subscriptions,
            "t": t
        }
        # "m": "compact_marketdata"
        self.ws.send(json.dumps(data))

    def unsubscribe(self, instrument):
        global split_subscribes
        scripts = ""
        if self.subscriptions:
            split_subscribes = self.subscriptions.split('#')
        for __instrument in instrument:
            scripts = scripts + __instrument.exchange + "|" + str(__instrument.token) + "#"
            if self.subscriptions:
                split_subscribes.remove(__instrument.exchange + "|" + str(__instrument.token))
        self.subscriptions = split_subscribes

        if self.market_depth:
            t = "ud"
        else:
            t = "u"

        data = {
            "k": scripts[:-1],
            "t": t
        }
        self.ws.send(json.dumps(data))

    def start_websocket(self, socket_open_callback=None, socket_close_callback=None, socket_error_callback=None,
                        subscription_callback=None, check_subscription_callback=None, run_in_background=False,
                        market_depth=False):
        if check_subscription_callback != None:
            check_subscription_callback(self.script_subscription_instrument)
        session_request = self._session_id
        self.__on_open = socket_open_callback
        self.__on_disconnect = socket_close_callback
        self.__on_error = socket_error_callback
        self.__subscribe_callback = subscription_callback

        self.market_depth = market_depth
        if self.__stop_event != None and self.__stop_event.is_set():
            self.__stop_event.clear()
        if session_request:
            session_id = session_request

            first_hash = hashlib.sha256(session_id.encode('utf-8')).hexdigest()
            self.ENC = hashlib.sha256(first_hash.encode('utf-8')).hexdigest()

            invalidSess = self.invalid_sess(session_id)
            if invalidSess['status'] == 'Ok':
                print("STAGE 1: Invalidate the previous session :", invalidSess['status'])
                createSess = self.createSession(session_id)

                if createSess['status'] == 'Ok':
                    print("STAGE 2: Create the new session :", createSess['status'])
                    print("Connecting to Socket ...")
                    self.__stop_event = threading.Event()
                    websocket.enableTrace(False)
                    self.ws = websocket.WebSocketApp(self.websocket_url,
                                                     on_open=self.on_open,
                                                     on_message=self.on_message,
                                                     on_close=self.on_close,
                                                     on_error=self.on_error)

                    if run_in_background is True:
                        self.__ws_thread = threading.Thread(target=self.__ws_run_forever)
                        self.__ws_thread.daemon = True
                        self.__ws_thread.start()
                    else:
                        self.__ws_run_forever()


"""Web Socket Handler"""
