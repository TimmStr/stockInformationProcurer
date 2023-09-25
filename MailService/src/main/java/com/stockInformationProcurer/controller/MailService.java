/**
 * The `MailService` class is responsible for sending emails with attachments.
 * It uses the JavaMailSender to send emails using the configured mail server.
 */
package com.stockInformationProcurer.controller;

import jakarta.mail.internet.MimeMessage;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.mail.MailAuthenticationException;
import org.springframework.mail.MailException;
import org.springframework.mail.MailParseException;
import org.springframework.mail.MailSendException;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.stereotype.Service;

@Service
public class MailService {

    private final JavaMailSender javaMailSender;

    @Autowired
    public MailService(JavaMailSender javaMailSender) {
        this.javaMailSender = javaMailSender;
    }

    /**
     * Sends an email with an attachment to the specified recipient.
     *
     * @param to             The recipient's email address.
     * @param subject        The subject of the email.
     * @param text           The content of the email.
     * @param attachment     The byte array representing the attachment.
     * @param attachmentName The name of the attachment.
     * @throws RuntimeException If there is an issue with sending the email, parsing email content,
     *                          authentication failure, or unexpected errors.
     */
    public void sendEmail(String to, String subject, String text, byte[] attachment, String attachmentName) {
        try {
            // Create a new MimeMessage for email composition.
            MimeMessage message = javaMailSender.createMimeMessage();

            // Use MimeMessageHelper to assist in creating a multipart email.
            MimeMessageHelper helper = new MimeMessageHelper(message, true);

            // Set the recipient's email address, email subject, and email content.
            helper.setTo(to);
            helper.setSubject(subject);
            helper.setText(text, true);

            // Add an attachment to the email.
            helper.addAttachment(attachmentName, new ByteArrayResource(attachment));

            // Send the email using the configured JavaMailSender.
            javaMailSender.send(message);

        } catch (MailParseException e) {
            e.printStackTrace();
            throw new RuntimeException("Failed to parse email content", e);
        } catch (MailAuthenticationException e) {
            e.printStackTrace();
            throw new RuntimeException("Authentication failed", e);
        } catch (MailSendException e) {
            e.printStackTrace();
            throw new RuntimeException("Failed to send email", e);
        } catch (MailException e) {
            e.printStackTrace();
            throw new RuntimeException("Mail error", e);
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException("Unexpected error", e);
        }
    }
}
