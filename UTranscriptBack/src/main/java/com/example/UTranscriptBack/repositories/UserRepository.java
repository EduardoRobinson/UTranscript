package com.example.UTranscriptBack.repositories;
import org.springframework.data.jpa.repository.JpaRepository;
import com.example.UTranscriptBack.models.UserModel;
import java.util.Optional;
public interface UserRepository extends JpaRepository<UserModel, Long>{
    Optional<UserModel> findByEmail(String email);
}
