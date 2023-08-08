//
//
//import com.stockInformationProcurer.services.ProcureStockInformationService;
//import org.apache.http.client.methods.CloseableHttpResponse;
//import org.apache.http.client.methods.HttpGet;
//import org.apache.http.impl.client.CloseableHttpClient;
//import org.junit.Before;
//import org.junit.Test;
//import org.junit.runner.RunWith;
//import org.mockito.Mock;
//import org.mockito.junit.MockitoJUnitRunner;
//import org.springframework.boot.test.context.SpringBootTest;
//import org.springframework.boot.test.mock.mockito.MockBean;
//
//import static org.junit.Assert.assertEquals;
//import static org.mockito.Mockito.*;
//
//@RunWith(MockitoJUnitRunner.class)
//@SpringBootTest
//public class ProcureStockInformationServiceTest {
//
////    private static final String DUMMY_API_KEY = "dummy_api_key";
////    private static final String DUMMY_SYMBOL = "AAPL";
////    private static final String DUMMY_RESPONSE = "{ \"Time Series\": { \"2023-08-07\": { \"1. open\": \"148.5600\", \"2. high\": \"149.5495\", \"3. low\": \"147.5500\", \"4. close\": \"148.4800\", \"5. volume\": \"4860100\" } } }";
////
////    @MockBean
////    private CloseableHttpClient httpClient;
////
////    @Mock
////    private CloseableHttpResponse httpResponse;
////
////    private ProcureStockInformationService stockInformationProcurer;
////
////    @Before
////    public void setUp() throws Exception {
////        stockInformationProcurer = new ProcureStockInformationService(DUMMY_API_KEY, DUMMY_SYMBOL);
////    }
////
////    @Test
////    public void testGetStockInformation_Success() throws Exception {
////        // Arrange
////        String apiUrl = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=dummy_api_key";
////        when(httpClient.execute(any(HttpGet.class))).thenReturn(httpResponse);
////        when(httpResponse.getEntity()).thenReturn(httpResponse.getEntity());
////
////        // Act
////        String stockInformation = stockInformationProcurer.getStockInformation();
////
////        // Assert
////        assertEquals(DUMMY_RESPONSE, stockInformation);
////        verify(httpClient, times(1)).execute(any(HttpGet.class));
////    }
////
////    @Test
////    public void testGetStockInformation_Exception() throws Exception {
////        // Arrange
////        when(httpClient.execute(any(HttpGet.class))).thenThrow(new RuntimeException("Test Exception"));
////
////        // Act
////        String stockInformation = stockInformationProcurer.getStockInformation();
////
////        // Assert
////        assertEquals(null, stockInformation);
////        verify(httpClient, times(1)).execute(any(HttpGet.class));
////    }
//}
