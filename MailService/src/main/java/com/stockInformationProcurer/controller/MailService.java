/**
 * The 'MailService' class provides methods to send and receive emails.
 * It allows users to send emails with attachments, set email content,
 * and manage email recipients. This service uses a specified email server
 * for sending and receiving emails.
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

    public void sendEmail(String to, String subject, String text, byte[] attachment, String attachmentName) {
        try {
            MimeMessage message = javaMailSender.createMimeMessage();
            MimeMessageHelper helper = new MimeMessageHelper(message, true);
            helper.setTo(to);
            helper.setSubject(subject);
            helper.setText(text, true); // Enable HTML content if needed
            helper.addAttachment(attachmentName, new ByteArrayResource(attachment));

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
