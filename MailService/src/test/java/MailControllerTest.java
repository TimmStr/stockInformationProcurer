import com.stockInformationProcurer.controller.MailController;
import com.stockInformationProcurer.services.MailService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.web.multipart.MultipartFile;

import java.nio.charset.StandardCharsets;

import static org.mockito.Mockito.doNothing;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

public class MailControllerTest {

    private MockMvc mockMvc;

    @Mock
    private MailService mailService;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
        this.mockMvc = MockMvcBuilders.standaloneSetup(new MailController(mailService)).build();
    }

//    @Test
//    public void testSendMail() throws Exception {
//        // Prepare test data
//        String to = "recipient@example.com";
//        String subject = "Test Subject";
//        String text = "Test Content";
//        String filename = "test.txt";
//        MultipartFile file = new MockMultipartFile(filename, "This is a test file content.".getBytes(StandardCharsets.UTF_8));
//
//        // Mock the behavior of mailService
//        doNothing().when(mailService).sendEmail(to, subject, text, file.getBytes(), filename);
//
//        // Perform the POST request
//        mockMvc.perform(fileUpload("/mail/sendMail")
//                        .file("file", file.getBytes())
//                        .param("to", to)
//                        .param("subject", subject)
//                        .param("text", text)
//                        .param("filename", filename)
//                        .contentType(MediaType.MULTIPART_FORM_DATA))
//                .andExpect(status().isOk());
//    }
}
