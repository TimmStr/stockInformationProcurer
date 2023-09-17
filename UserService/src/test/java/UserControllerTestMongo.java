import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

public class UserControllerTestMongo {
//
//    private UserController userController;
//
//    @Mock
//    private UserRepositoryService userRepositoryService;
//
//    @BeforeEach
//    public void setUp() {
//        MockitoAnnotations.initMocks(this);
//        userController = new UserController(userRepositoryService);
//    }
//
//    @Test
//    public void testWelcome() {
//        ResponseEntity response = userController.welcome();
//        assertEquals(HttpStatus.OK, response.getStatusCode());
//        assertEquals("User Controller works", response.getBody());
//    }
//
//    @Test
//    public void testAddUser() {
//        String firstname = "John";
//        String lastname = "Doe";
//        String mail = "john@example.com";
//        String password = "password";
//
//        ResponseEntity response = userController.addUser(firstname, lastname, mail, password);
//
//        assertEquals(HttpStatus.OK, response.getStatusCode());
//        assertEquals(lastname + " added.", response.getBody());
//
//        verify(userRepositoryService, times(1)).addUserInformation(any(UserEntity.class));
//    }
//
//    @Test
//    public void testGetUserInformation() {
//        String lastname = "Doe";
//        String userInformation = "User information for Doe";
//
//        when(userRepositoryService.getUserInformationForLastname(lastname)).thenReturn(userInformation);
//
//        ResponseEntity response = userController.getUserInformation(lastname);
//
//        assertEquals(HttpStatus.OK, response.getStatusCode());
//        assertEquals(userInformation, response.getBody());
//    }
//
//    @Test
//    public void testCheckUserWithValidCredentials() {
//        String mail = "peter.parker@gmail.com";
//        String password = "1245";
//
//        UserEntity user = new UserEntity("Peter", "Parker", mail, password);
//        List<UserEntity> users = Arrays.asList(user);
//
//        when(userRepositoryService.findAll()).thenReturn(users);
//
//        ResponseEntity response = userController.checkUser(mail, password);
//
//        assertEquals(HttpStatus.OK, response.getStatusCode());
//        assertEquals(user, response.getBody());
//    }
//
//    @Test
//    public void testCheckUserWithInvalidCredentials() {
//        String mail = "peter.parker@gmail.co";
//        String password = "987";
//
//        List<UserEntity> users = Arrays.asList(
//                new UserEntity("Peter", "Parker", mail, "876")
//        );
//
//        when(userRepositoryService.findAll()).thenReturn(users);
//
//        ResponseEntity response = userController.checkUser(mail, password);
//
//        assertEquals(HttpStatus.NOT_ACCEPTABLE, response.getStatusCode());
//        assertEquals("User not found", response.getBody());
//    }
}
