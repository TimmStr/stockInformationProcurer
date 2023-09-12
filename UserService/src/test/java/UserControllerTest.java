import com.stockInformationProcurer.controller.UserController;
import com.stockInformationProcurer.entity.User;
import com.stockInformationProcurer.services.UserService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.*;

public class UserControllerTest {

    @InjectMocks
    private UserController userController;

    @Mock
    private UserService userService;

    @BeforeEach
    public void init() {
        MockitoAnnotations.initMocks(this);
    }

    @Test
    public void testAddUser() {
        ResponseEntity responseEntity = userController.addUser("John", "Doe", "john@example.com", "password", true);

        assertEquals(HttpStatus.OK, responseEntity.getStatusCode());
        verify(userService, times(1)).createUser(any(User.class));
    }

    @Test
    public void testGetUserInformation() {
        User user = new User("John", "Doe", "john@example.com", "password", true);
        when(userService.getUserByLastname("Doe")).thenReturn(user);

        ResponseEntity responseEntity = userController.getUserInformation("Doe");

        assertEquals(HttpStatus.OK, responseEntity.getStatusCode());
        assertEquals(user.toString(), responseEntity.getBody());
    }

    @Test
    public void testGetAllUsers() {
        List<User> users = Arrays.asList(
                new User("John", "Doe", "john@example.com", "password", true),
                new User("Jane", "Smith", "jane@example.com", "password", true)
        );
        when(userService.getAllUsers()).thenReturn(users);

        ResponseEntity responseEntity = userController.getAllUsers();

        assertEquals(HttpStatus.OK, responseEntity.getStatusCode());
        assertEquals(users, responseEntity.getBody());
    }

//    @Test
//    public void testCheckUserFound() {
//        User user = new User("John", "Doe", "john@example.com", "password");
//        List<User> users = Arrays.asList(user);
//
//        when(userService.getAllUsers()).thenReturn(users);
//
//        ResponseEntity responseEntity = userController.checkUser("john@example.com", "password");
//
//        assertEquals(HttpStatus.OK, responseEntity.getStatusCode());
//        assertEquals(user, responseEntity.getBody());
//    }

    @Test
    public void testCheckUserNotFound() {
        List<User> users = Arrays.asList(
                new User("John", "Doe", "john@example.com", "password", true),
                new User("Jane", "Smith", "jane@example.com", "password", true)
        );

        when(userService.getAllUsers()).thenReturn(users);

        ResponseEntity responseEntity = userController.checkUser("notfound@example.com", "wrongpassword");

        assertEquals(HttpStatus.NOT_ACCEPTABLE, responseEntity.getStatusCode());
        assertEquals("User not found", responseEntity.getBody());
    }
}
