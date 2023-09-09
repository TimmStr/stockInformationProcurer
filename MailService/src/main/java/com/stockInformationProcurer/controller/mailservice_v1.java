import java.util.Properties;
import javax.mail.*;
import javax.mail.internet.*;

public class SimpleMailService {

    public static void main(String[] args) {
        // Konfigurieren Sie die Mail-Einstellungen
        String smtpHost = "smtp.example.com"; // SMTP-Server
        String smtpPort = "587"; // SMTP-Port
        String username = "your_username";
        String password = "your_password";
        String fromAddress = "your_email@example.com";
        String toAddress = "recipient@example.com";

        // Erstellen Sie eine Sitzung mit den Mail-Einstellungen
        Properties props = new Properties();
        props.put("mail.smtp.host", smtpHost);
        props.put("mail.smtp.port", smtpPort);
        props.put("mail.smtp.auth", "true");
        props.put("mail.smtp.starttls.enable", "true");

        Session session = Session.getInstance(props, new Authenticator() {
            @Override
            protected PasswordAuthentication getPasswordAuthentication() {
                return new PasswordAuthentication(username, password);
            }
        });

        try {
            // Erstellen Sie eine neue Nachricht
            Message message = new MimeMessage(session);
            message.setFrom(new InternetAddress(fromAddress));
            message.setRecipient(Message.RecipientType.TO, new InternetAddress(toAddress));
            message.setSubject("Test-E-Mail");
            message.setText("Dies ist eine Testnachricht von Ihrem Java-Mail-Service.");

            // Senden Sie die Nachricht
            Transport.send(message);

            System.out.println("Die E-Mail wurde erfolgreich gesendet.");

        } catch (MessagingException e) {
            e.printStackTrace();
            System.err.println("Fehler beim Senden der E-Mail: " + e.getMessage());
        }
    }
}
