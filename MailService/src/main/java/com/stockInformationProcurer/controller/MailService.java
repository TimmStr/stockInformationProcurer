/**
 * The 'MailService' class provides methods to send and receive emails.
 * It allows users to send emails with attachments, set email content,
 * and manage email recipients. This service uses a specified email server
 * for sending and receiving emails.
*/
package com.stockInformationProcurer.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.mail.MailException;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.stereotype.Service;

import javax.mail.MessagingException;
import javax.mail.internet.MimeMessage;

@Service
public class MailService {

    private final JavaMailSender javaMailSender;
    
    @Autowired
    public MailService(JavaMailSender javaMailSender) {
        this.javaMailSender = javaMailSender;
    }

    public void sendEmail(String to, String subject, String text) {
    try {
        MimeMessage message = javaMailSender.createMimeMessage();
        MimeMessageHelper helper = new MimeMessageHelper(message, true);
        helper.setTo(to);
        helper.setSubject(subject);
        helper.setText(text, true); // Enable HTML content if needed

        javaMailSender.send(message);
    } catch (MailParseException e) {
        e.printStackTrace();
        throw new RuntimeException("Failed to parse email content", e);
    } catch (MessagingException e) {
        e.printStackTrace();
        throw new RuntimeException("Failed to create email message", e);
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
