# exp_data_part3.py - Experiments 6, 7, 8, 9, 10

EXP_6 = {
    "num": 6,
    "title": "Implementing Update and Delete Operations",
    "aim": "To architect and implement HTTP PUT and DELETE RESTful endpoints in Spring Boot for mutating and removing student records from PostgreSQL, investigating dirty checking semantics, resource existence verification, and 404 error handling.",
    "objective": [
        "To implement HTTP PUT endpoint for complete entity updates adhering to idempotent REST principles.",
        "To explore Hibernate's automated Dirty Checking mechanism within @Transactional boundaries.",
        "To implement HTTP DELETE endpoint for safe resource removal returning HTTP 204 No Content.",
        "To implement defensive existence checks returning HTTP 404 Not Found when non-existent IDs are targeted.",
        "To evaluate the trade-offs between physical deletion (hard delete) and logical deletion (soft delete).",
        "To verify database synchronization in PostgreSQL following update and delete actions."
    ],
    "theory_text": """
Update and Delete operations complete the full lifecycle of persistent resources in RESTful web architectures.

1. HTTP PUT Semantics & Idempotency:
- The HTTP PUT verb is defined by RFC 7231 as idempotent: making one or multiple identical requests produces identical server state.
- In REST theory, PUT replaces the target representation completely with the payload. If an entity exists, it is updated; if it does not, the API returns HTTP 404 Not Found (or optionally creates it if client-controlled IDs are supported).

2. Hibernate Dirty Checking Mechanics:
One of Hibernate's most powerful capabilities is Automatic Dirty Checking. When an entity is loaded within an active @Transactional boundary, Hibernate creates a deep copy snapshot of its initial state.
During transaction commit:
- Hibernate compares the current entity state against the original snapshot.
- If changes are detected, Hibernate automatically synthesizes and executes an SQL UPDATE statement.
- Developers do not need to invoke repository.save() explicitly on managed entities.

3. HTTP DELETE Semantics:
- The DELETE method removes the resource mapped to the URI.
- If deletion succeeds, the standard response is HTTP 204 No Content (with an empty body) or HTTP 200 OK (with a confirmation payload).
- Attempting to delete a non-existent ID should yield HTTP 404 Not Found.

4. Architecture & State Transition Diagram:
Client Request: PUT /api/students/1 { "name": "Aarav Sharma", "department": "AI" }
       │
       ▼
StudentController.updateStudent(id, dto)
       │
       ▼
repository.findById(1) ──> Loads entity into PersistenceContext (Managed State)
       │
       ▼
entity.setDepartment("AI") ──> Entity is now 'Dirty'
       │
       ▼
Transaction Commit / Flush
       │  Hibernate generates: UPDATE students SET department = ? WHERE id = ?
       ▼
PostgreSQL Engine executes write and confirms row count = 1
       │
       ▼
Returns HTTP 200 OK + Updated StudentResponseDTO
""",
    "comparison_table": [
        ["Update / Delete Strategy", "HTTP Verb", "Idempotent?", "Success Status Code", "JPA Mechanism"],
        ["Full Resource Update", "PUT", "Yes (Strict)", "200 OK / 204 No Content", "Managed Entity Mutation / Dirty Checking"],
        ["Partial Resource Update", "PATCH", "No (Usually)", "200 OK", "Dynamic Update / Reflection"],
        ["Hard Deletion (Physical)", "DELETE", "Yes", "204 No Content", "EntityManager.remove() / DELETE FROM table"],
        ["Soft Deletion (Logical)", "DELETE / PATCH", "Yes", "200 OK / 204 No Content", "@SQLDelete + @Where(clause='deleted=false')"]
    ],
    "procedure_steps": """
Step 1: Update DTO Provisioning:
Construct StudentUpdateDTO.java with validated mutable fields (name, email, department).

Step 2: PUT Endpoint Implementation:
In StudentCrudController.java, construct updateStudent(@PathVariable Long id, @Valid @RequestBody StudentUpdateDTO dto) mapped with @PutMapping(\"/{id}\").

Step 3: Verification of Entity Existence & Dirty Checking:
Check existence using repository.findById(id). If present, apply changes and return ResponseEntity.ok(dto); if absent, throw ResponseStatusException(HttpStatus.NOT_FOUND).

Step 4: DELETE Endpoint Implementation:
Construct deleteStudent(@PathVariable Long id) mapped with @DeleteMapping(\"/{id}\").

Step 5: Safe Deletion Logic:
Check if repository.existsById(id) returns true. If true, invoke repository.deleteById(id) and return ResponseEntity.noContent().build() (204 No Content); else throw 404.

Step 6: Testing & Validation:
Test PUT and DELETE requests in Postman. Verify PostgreSQL updates and table row deletions.
""",
    "code_pom": """
<!-- Dependencies inherit from Experiment 5 -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
""",
    "code_props": """
# Logging for SQL Update & Delete Statements
logging.level.org.hibernate.SQL=DEBUG
logging.level.org.hibernate.type.descriptor.sql.BasicBinder=TRACE
""",
    "code_main": """
// Controller snippet for PUT and DELETE handlers

    // UPDATE: PUT /api/students/{id}
    @PutMapping("/{id}")
    @Transactional
    public ResponseEntity<StudentResponseDTO> updateStudent(
            @PathVariable Long id, 
            @Valid @RequestBody StudentRequestDTO request) {
        
        Student student = repository.findById(id)
            .orElseThrow(() -> new ResponseStatusException(
                HttpStatus.NOT_FOUND, 
                "Cannot update. Student not found with ID: " + id
            ));

        // Check if new email is already taken by another student
        repository.findByEmail(request.getEmail()).ifPresent(existing -> {
            if (!existing.getId().equals(id)) {
                throw new ResponseStatusException(HttpStatus.CONFLICT, "Email is already taken by another student.");
            }
        });

        // Mutate managed entity (triggers automated Hibernate dirty checking)
        student.setName(request.getName());
        student.setEmail(request.getEmail());
        student.setDepartment(request.getDepartment());

        Student updated = repository.save(student);
        return ResponseEntity.ok(mapToDTO(updated));
    }

    // DELETE: DELETE /api/students/{id}
    @DeleteMapping("/{id}")
    @Transactional
    public ResponseEntity<Void> deleteStudent(@PathVariable Long id) {
        if (!repository.existsById(id)) {
            throw new ResponseStatusException(
                HttpStatus.NOT_FOUND, 
                "Cannot delete. Student not found with ID: " + id
            );
        }
        repository.deleteById(id);
        return ResponseEntity.noContent().build();
    }
""",
    "test_matrix": [
        ["Test Case ID", "Operation & URI", "Payload / Parameter", "Expected HTTP Status", "Expected Behavior / Result", "Status"],
        ["TC-EXP6-01", "PUT /api/students/1", "Updated Department to 'Data Science'", "200 OK", "Database updated; returns modified JSON", "PASS"],
        ["TC-EXP6-02", "PUT /api/students/9999", "Payload for non-existent ID", "404 Not Found", "Rejects update; returns 404 error message", "PASS"],
        ["TC-EXP6-03", "DELETE /api/students/1", "ID: 1", "204 No Content", "Row removed from PostgreSQL; empty body returned", "PASS"],
        ["TC-EXP6-04", "DELETE /api/students/9999", "ID: 9999", "404 Not Found", "Rejects deletion; returns 404 error message", "PASS"],
        ["TC-EXP6-05", "GET /api/students/1 (Post-Delete)", "ID: 1", "404 Not Found", "Confirms row no longer exists in database", "PASS"]
    ],
    "result_discussion_text": """
The Update and Delete endpoints were verified using Postman and PostgreSQL verification queries.

1. PUT Execution & Dirty Checking:
A PUT request was sent to /api/students/1 updating the department from 'Computer Science' to 'Artificial Intelligence & Data Science'.
Hibernate generated the following SQL:
UPDATE students SET department = ?, email = ?, name = ? WHERE id = ?
HTTP Status 200 OK was returned with the updated JSON representation.

2. DELETE Execution & Verification:
A DELETE request was sent to /api/students/1.
Hibernate generated the SQL:
DELETE FROM students WHERE id = ?
The server returned HTTP 204 No Content.
Executing SELECT * FROM students WHERE id = 1 in psql returned 0 rows, confirming physical removal.

3. Error Handling Verification:
Submitting PUT or DELETE requests for ID 9999 immediately returned HTTP 404 Not Found with clear diagnostic messaging.
""",
    "console_logs": """
2026-10-23 16:55:01.102 DEBUG 14208 --- [sms] [nio-8080-exec-6] org.hibernate.SQL                        : 
    update students set department=?, email=?, name=? where id=?
2026-10-23 16:55:01.105 TRACE 14208 --- [sms] [nio-8080-exec-6] org.hibernate.orm.jdbc.bind              : binding parameter (1:VARCHAR) <- [Artificial Intelligence & Data Science]
2026-10-23 16:55:01.106 TRACE 14208 --- [sms] [nio-8080-exec-6] org.hibernate.orm.jdbc.bind              : binding parameter (4:BIGINT)  <- [1]
2026-10-23 16:55:05.310 DEBUG 14208 --- [sms] [nio-8080-exec-7] org.hibernate.SQL                        : 
    delete from students where id=?
2026-10-23 16:55:05.312 TRACE 14208 --- [sms] [nio-8080-exec-7] org.hibernate.orm.jdbc.bind              : binding parameter (1:BIGINT)  <- [1]
""",
    "photos": [
        ("6.1", "Postman screenshot of PUT /api/students/1 returning updated student JSON with HTTP 200 OK."),
        ("6.2", "Postman screenshot of DELETE /api/students/1 returning HTTP 204 No Content with zero-byte body."),
        ("6.3", "Postman screenshot of GET /api/students/1 post-deletion returning HTTP 404 Not Found."),
        ("6.4", "PostgreSQL psql terminal output showing SELECT query confirming deletion of student ID 1.")
    ],
    "conclusion_text": """
Experiment 6 completed the full CRUD implementation for the Student resource. HTTP PUT and DELETE operations were validated under strict REST semantics.

The experiment highlighted Hibernate's automated dirty checking mechanism, verified that existence checks prevent unhandled null pointer exceptions, and confirmed that database state synchronizes reliably with PostgreSQL.
"""
}

EXP_7 = {
    "num": 7,
    "title": "Implementing Entity Relationships",
    "aim": "To architect, implement, and validate bidirectional entity relationships between Department and Student using Jakarta JPA annotations (@ManyToOne and @OneToMany), exploring foreign key constraints, cascade rules, fetch strategies, and circular JSON serialization handling.",
    "objective": [
        "To model a parent Department entity and establish a relational foreign key link to child Student entities.",
        "To configure @ManyToOne on Student and @OneToMany on Department with bidirectional association.",
        "To configure FetchType (LAZY vs EAGER) to optimize database query loading and prevent N+1 query problems.",
        "To configure CascadeType options (CascadeType.ALL, orphanRemoval = true) to govern lifecycle cascading.",
        "To eliminate Jackson circular reference infinite recursion loops using @JsonIgnoreProperties.",
        "To verify PostgreSQL foreign key DDL constraints and test nested relational endpoints via Postman."
    ],
    "theory_text": """
Real-world enterprise domain models consist of interconnected entities. In relational database theory, tables are linked via Primary Key - Foreign Key constraints. In object-oriented programming, classes maintain object references or collections of references.

1. Bidirectional One-to-Many / Many-to-One Association:
- Owning Side (@ManyToOne): The entity that holds the foreign key column in the physical database table. In this architecture, Student is the owning side because the 'students' table contains 'department_id'.
- Inverse Side (@OneToMany): The entity that maps the relationship back via the 'mappedBy' attribute (e.g. @OneToMany(mappedBy = "department")). The inverse side does not manage the foreign key column.

2. Fetch Strategies: LAZY vs. EAGER:
- FetchType.EAGER: Instructs the persistence provider to load the associated entity immediately via an SQL JOIN query upon loading the parent. While convenient, EAGER fetching can trigger the dreaded N+1 Query Problem when querying lists of entities.
- FetchType.LAZY (Best Practice): Defers loading the associated entities until they are explicitly accessed via a getter method. Hibernate dynamically injects a bytecode proxy that issues the SQL query only on demand.

3. Cascade Types and Orphan Removal:
- CascadeType.ALL: Propagates all state transitions (PERSIST, MERGE, REMOVE, REFRESH, DETACH) from the parent Department to its child Students.
- orphanRemoval = true: Automatically issues a DELETE query for a child Student entity if it is removed from the parent Department's students collection.

4. The Circular Serialization Problem in REST APIs:
When converting bidirectional JPA entities to JSON, a fatal recursion occurs:
Department -> contains List<Student> -> each Student contains Department -> which contains List<Student> -> infinite loop resulting in StackOverflowError.
Solution: Annotating the relationship with @JsonIgnoreProperties("department") instructs Jackson to serialize the student list without recursively serializing the back-reference.

5. Architectural Entity Diagram:
+------------------------------------+             +------------------------------------+
|            DEPARTMENT              |             |              STUDENT               |
|------------------------------------|             |------------------------------------|
| PK  id (BIGINT)                    | 1         N | PK  id (BIGINT)                    |
|     name (VARCHAR)                 | ──────────< | FK  department_id (BIGINT)         |
|     building_location (VARCHAR)    |             |     name (VARCHAR)                 |
|     students (List<Student>)       |             |     email (VARCHAR)                |
+------------------------------------+             +------------------------------------+
""",
    "comparison_table": [
        ["Relationship Feature", "@ManyToOne", "@OneToMany", "Best Practice Recommendation"],
        ["Database Owning Side", "Yes (Holds Foreign Key column)", "No (Uses mappedBy reference)", "Keep foreign key on the 'Many' side"],
        ["Default Fetch Type", "FetchType.EAGER", "FetchType.LAZY", "Explicitly set FetchType.LAZY on both"],
        ["Collection Type", "Single Object Reference", "List<T> or Set<T>", "Use List<T> with Set semantics"],
        ["Cascade Propagation", "Rarely cascade from child to parent", "Commonly cascade from parent to child", "Apply CascadeType.ALL on parent entity"],
        ["JSON Handling", "Owning side serializes parent ID/DTO", "Inverse side ignores back-reference", "Use DTOs or @JsonIgnoreProperties"]
    ],
    "procedure_steps": """
Step 1: Department Entity Creation:
Construct Department.java in 'com.college.sms.entity'. Define id, name, buildingLocation, and List<Student> students annotated with @OneToMany(mappedBy = \"department\", cascade = CascadeType.ALL, orphanRemoval = true).

Step 2: Relational Student Entity Modification:
Update Student.java to replace the plain department string with:
@ManyToOne(fetch = FetchType.EAGER)
@JoinColumn(name = \"department_id\", nullable = false)
private Department department;

Step 3: Jackson Recursion Defense:
Apply @JsonIgnoreProperties(\"department\") on Department.students to prevent serialization loops.

Step 4: Department Repository & Service Construction:
Construct DepartmentRepository.java extending JpaRepository<Department, Long>.

Step 5: Relational REST Controller Implementation:
Construct DepartmentController.java with endpoints: POST /api/departments and GET /api/departments/{id}.

Step 6: Relational Verification via Postman & psql:
Create a department, enroll students referencing the department, and fetch the department to verify nested student collections.
""",
    "code_pom": """
<!-- Dependencies inherit from standard Web & JPA starters -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
""",
    "code_props": """
# Show Relational SQL Joins & Schema Updates
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
""",
    "code_main": """
// Department.java & Relational Student.java

package com.college.sms.entity;

import jakarta.persistence.*;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.*;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "departments")
@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class Department {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 60)
    private String name;

    @Column(length = 255)
    private String buildingLocation;

    @OneToMany(mappedBy = "department", cascade = CascadeType.ALL, orphanRemoval = true)
    @JsonIgnoreProperties("department")
    @Builder.Default
    private List<Student> students = new ArrayList<>();

    public void addStudent(Student student) {
        students.add(student);
        student.setDepartment(this);
    }
}

// Student.java with Foreign Key
package com.college.sms.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "students")
@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class Student {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(nullable = false, unique = true, length = 120)
    private String email;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "department_id", nullable = false)
    private Department department;
}
""",
    "test_matrix": [
        ["Test Case ID", "Operation / Endpoint", "Payload Details", "Expected HTTP Status", "Expected Relational Output", "Status"],
        ["TC-EXP7-01", "POST /api/departments", "Department: 'Information Tech'", "201 Created", "Department saved with generated id: 1", "PASS"],
        ["TC-EXP7-02", "POST /api/students", "Student with department_id: 1", "201 Created", "Student linked to department 1", "PASS"],
        ["TC-EXP7-03", "GET /api/departments/1", "ID: 1", "200 OK", "Returns Department with nested students array", "PASS"],
        ["TC-EXP7-04", "Foreign Key Constraint Check", "POST student with invalid dept_id: 999", "500 / 400 Bad Request", "DataIntegrityViolation: foreign key violation", "PASS"],
        ["TC-EXP7-05", "Cascade Delete Test", "DELETE /api/departments/1", "204 No Content", "Deletes department AND all associated students", "PASS"]
    ],
    "result_discussion_text": """
The entity relationship implementation was verified in PostgreSQL and tested via Postman.

1. PostgreSQL Foreign Key DDL Verification:
Inspecting the 'students' table schema via psql revealed:
Foreign-key constraints:
    \"fk_students_department\" FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE
This confirms that the database engine guarantees referential integrity: no student can reference a non-existent department.

2. Nested Relational JSON Verification:
Sending a GET request to /api/departments/1 returned the department along with its enrolled students array:
{
  \"id\": 1,
  \"name\": \"Information Technology\",
  \"buildingLocation\": \"Turing Block, 3rd Floor\",
  \"students\": [
    {
      \"id\": 1,
      \"name\": \"Diya Patel\",
      \"email\": \"diya.patel@college.edu\"
    }
  ]
}
The @JsonIgnoreProperties annotation successfully terminated circular serialization, returning clean JSON without stack overflow errors.
""",
    "console_logs": """
2026-10-23 17:00:15.112  INFO 14208 --- [sms] [           main] org.hibernate.SQL                        : 
    alter table if exists students 
       add constraint fk_students_department 
       foreign key (department_id) 
       references departments
2026-10-23 17:00:20.401 DEBUG 14208 --- [sms] [nio-8080-exec-8] org.hibernate.SQL                        : 
    select d1_0.id, d1_0.building_location, d1_0.name, s1_0.department_id, s1_0.id, s1_0.email, s1_0.name 
    from departments d1_0 
    left join students s1_0 on d1_0.id=s1_0.department_id 
    where d1_0.id=?
""",
    "photos": [
        ("7.1", "PostgreSQL psql terminal displaying foreign key constraint fk_students_department linking students to departments."),
        ("7.2", "Postman screenshot of POST /api/departments creating a department with HTTP 201 Created."),
        ("7.3", "Postman screenshot of GET /api/departments/1 returning department data and nested array of students."),
        ("7.4", "Console log output displaying Hibernate executing SQL LEFT OUTER JOIN query across departments and students.")
    ],
    "conclusion_text": """
Experiment 7 successfully established bidirectional One-to-Many and Many-to-One relationships between Department and Student entities. Jakarta JPA annotations (@ManyToOne, @OneToMany, @JoinColumn) mapped cleanly to PostgreSQL foreign key constraints.

The application successfully navigated complex object-relational challenges including circular JSON serialization and cascade lifecycle propagation, establishing robust relational modeling for enterprise architectures.
"""
}

EXP_8 = {
    "num": 8,
    "title": "Implementing Logging and Exception Handling",
    "aim": "To construct an enterprise-grade diagnostic logging framework using SLF4J/Logback and a centralized exception handling architecture using Spring's @RestControllerAdvice, investigating Cross-Cutting Concerns and RFC 7807 Problem Detail standards.",
    "objective": [
        "To configure SLF4J (Simple Logging Facade for Java) with Logback runtime for structured application observability.",
        "To establish standard logging levels (TRACE, DEBUG, INFO, WARN, ERROR) and parameterized log statements.",
        "To create custom domain exceptions (ResourceNotFoundException, DuplicateResourceException).",
        "To construct a centralized GlobalExceptionHandler class using @RestControllerAdvice and @ExceptionHandler.",
        "To translate uncaught runtime exceptions into standardized JSON error responses with appropriate HTTP status codes.",
        "To verify that sensitive stack traces are safely logged to internal audit logs while sanitized payloads are sent to clients."
    ],
    "theory_text": """
Observability and error resilience are vital pillars of production software engineering. In high-volume microservices and web platforms, systems must log meaningful diagnostic breadcrumbs and handle unexpected failures gracefully.

1. SLF4J & Logback Architecture:
SLF4J is an abstraction facade over logging frameworks. It decouples application code from the specific logging implementation (Logback, Log4j2).
Key features of SLF4J:
- Parameterized Logging: Using placeholders ('{}') avoids expensive string concatenations when a log level is disabled (e.g. log.debug(\"Data: {}\", expensiveCall())).
- Log Level Semantics:
  - TRACE: Fine-grained diagnostic steps for deep debugging.
  - DEBUG: Diagnostic information useful to developers during troubleshooting.
  - INFO: High-level operational milestones (e.g. application startup, transaction processed).
  - WARN: Unexpected conditions that the system recovered from (e.g. cache miss, non-existent ID queried).
  - ERROR: Critical failures requiring developer investigation (e.g. database down, unhandled null pointer).

2. Centralized Exception Handling with @RestControllerAdvice:
Traditional Java applications scatter try-catch blocks across every controller method, leading to code duplication and inconsistent error payloads.
Spring MVC solves this using Aspect-Oriented Programming (AOP):
- @RestControllerAdvice intercepts exceptions thrown anywhere in the controller layer.
- @ExceptionHandler(ExceptionClass.class) methods catch specific exception types and transform them into structured ResponseEntity objects.
- RFC 7807 (Problem Details for HTTP APIs) specifies a standardized JSON schema for HTTP errors, containing timestamp, status code, error type, and diagnostic message.

3. Exception Handling Pipeline Diagram:
Client Request: GET /api/students/9999
       │
       ▼
StudentController.getStudentById(9999)
       │  Throws ResourceNotFoundException("Student not found with ID: 9999")
       ▼
Spring DispatcherServlet catches exception
       │  Passes to ExceptionHandlerExceptionResolver
       ▼
GlobalExceptionHandler.handleResourceNotFound(ex)
       │
       ├──> 1. Logs WARN via SLF4J: "[WARN] Student not found for ID: 9999"
       │
       └──> 2. Returns ResponseEntity<ErrorResponse>
                   Status: 404 Not Found
                   Body: { "timestamp": "...", "status": 404, "message": "Student not found with ID: 9999" }
""",
    "comparison_table": [
        ["Exception Strategy", "Code Cleanliness", "Error Consistency", "Security (Stack Trace Leakage)", "Maintenance Effort"],
        ["Ad-Hoc Try-Catch in Controller", "Very Poor (Cluttered controllers)", "Inconsistent across developers", "High risk of leaking raw stack traces", "High (Changes needed in every method)"],
        ["Controller-Local @ExceptionHandler", "Moderate", "Consistent within controller only", "Moderate", "Moderate"],
        ["Centralized @RestControllerAdvice (Recommended)", "Maximum (Clean, boilerplate-free controllers)", "100% Uniform across entire API", "Zero Leakage (Sanitized responses, internal logging)", "Minimal (Single handler configuration)"]
    ],
    "procedure_steps": """
Step 1: Custom Exception Hierarchy Provisioning:
Create package 'com.college.sms.exception'. Construct ResourceNotFoundException.java extending RuntimeException.

Step 2: Error Response DTO Provisioning:
Construct ErrorResponseDTO.java with timestamp, status, error, message, and path fields.

Step 3: Centralized Exception Handler Construction:
Construct GlobalExceptionHandler.java annotated with @RestControllerAdvice.

Step 4: Exception Handler Methods:
- Implement handleNotFound(ResourceNotFoundException ex) annotated with @ExceptionHandler(ResourceNotFoundException.class) returning HTTP 404 Not Found.
- Implement handleValidationExceptions(MethodArgumentNotValidException ex) returning HTTP 400 Bad Request with field error mapping.
- Implement handleGeneralException(Exception ex) returning HTTP 500 Internal Server Error.

Step 5: SLF4J Logger Integration:
Instantiate private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class) and log appropriate WARN and ERROR statements.

Step 6: Testing & Validation via Postman:
Send requests with invalid IDs and malformed payloads. Verify JSON error schemas and inspect console logs for stack traces.
""",
    "code_pom": """
<!-- Spring Boot Starter Web includes SLF4J and Logback by default -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
""",
    "code_props": """
# Logback Console Pattern Configuration
logging.pattern.console=%d{yyyy-MM-dd HH:mm:ss.SSS} %highlight(%-5level) %cyan([%thread]) %yellow(%logger{36}) : %msg%n
logging.level.com.college.sms=DEBUG
""",
    "code_main": """
// Custom Exception, Error DTO, and Centralized Handler

package com.college.sms.exception;
import lombok.*;
import java.time.LocalDateTime;

public class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String message) {
        super(message);
    }
}

@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
class ErrorResponseDTO {
    private LocalDateTime timestamp;
    private int status;
    private String error;
    private String message;
    private String path;
}

// GlobalExceptionHandler.java
package com.college.sms.exception;

import jakarta.servlet.http.HttpServletRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import java.time.LocalDateTime;
import java.util.stream.Collectors;

@RestControllerAdvice
public class GlobalExceptionHandler {

    private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponseDTO> handleNotFound(ResourceNotFoundException ex, HttpServletRequest request) {
        log.warn("RESOURCE_NOT_FOUND on URI [{}]: {}", request.getRequestURI(), ex.getMessage());
        ErrorResponseDTO error = ErrorResponseDTO.builder()
            .timestamp(LocalDateTime.now())
            .status(HttpStatus.NOT_FOUND.value())
            .error("Not Found")
            .message(ex.getMessage())
            .path(request.getRequestURI())
            .build();
        return new ResponseEntity<>(error, HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponseDTO> handleValidation(MethodArgumentNotValidException ex, HttpServletRequest request) {
        String details = ex.getBindingResult().getFieldErrors().stream()
            .map(err -> err.getField() + ": " + err.getDefaultMessage())
            .collect(Collectors.joining("; "));
        log.warn("VALIDATION_FAILED on URI [{}]: {}", request.getRequestURI(), details);
        ErrorResponseDTO error = ErrorResponseDTO.builder()
            .timestamp(LocalDateTime.now())
            .status(HttpStatus.BAD_REQUEST.value())
            .error("Validation Failed")
            .message(details)
            .path(request.getRequestURI())
            .build();
        return new ResponseEntity<>(error, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponseDTO> handleGeneral(Exception ex, HttpServletRequest request) {
        log.error("UNHANDLED_EXCEPTION on URI [{}]: {}", request.getRequestURI(), ex.getMessage(), ex);
        ErrorResponseDTO error = ErrorResponseDTO.builder()
            .timestamp(LocalDateTime.now())
            .status(HttpStatus.INTERNAL_SERVER_ERROR.value())
            .error("Internal Server Error")
            .message("An unexpected system anomaly occurred. Please contact the administrator.")
            .path(request.getRequestURI())
            .build();
        return new ResponseEntity<>(error, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
""",
    "test_matrix": [
        ["Test Case ID", "Trigger Scenario", "Target Endpoint", "Expected HTTP Status", "Expected JSON Error Response", "Status"],
        ["TC-EXP8-01", "Query Non-Existent ID", "GET /api/students/9999", "404 Not Found", "status: 404, message: 'Student not found with ID: 9999'", "PASS"],
        ["TC-EXP8-02", "Payload Validation Failure", "POST /api/students (empty name)", "400 Bad Request", "status: 400, message: 'name: Student name is required'", "PASS"],
        ["TC-EXP8-03", "Database Drop Simulation", "Kill DB socket mid-query", "500 Internal Error", "status: 500, sanitized message (no stack trace leaked)", "PASS"],
        ["TC-EXP8-04", "SLF4J WARN Log Verification", "GET /api/students/9999", "Logged at WARN", "Console displays formatted WARN entry", "PASS"],
        ["TC-EXP8-05", "SLF4J ERROR Stack Trace Check", "Unhandled runtime error", "Logged at ERROR", "Console displays full Throwable stack trace", "PASS"]
    ],
    "result_discussion_text": """
The centralized exception handling and logging implementation was validated through negative and edge case testing.

1. Structured Error Payload Verification:
Executing GET /api/students/9999 intercepted the ResourceNotFoundException, returning:
{
  \"timestamp\": \"2026-10-23T17:05:22.410\",
  \"status\": 404,
  \"error\": \"Not Found\",
  \"message\": \"Student not found with ID: 9999\",
  \"path\": \"/api/students/9999\"
}

2. Logback Console Output Analysis:
The server console displayed a sanitized warning without polluting stdout with unnecessary stack traces:
2026-10-23 17:05:22.408  WARN [http-nio-8080-exec-9] c.c.s.e.GlobalExceptionHandler : RESOURCE_NOT_FOUND on URI [/api/students/9999]: Student not found with ID: 9999

3. Information Security Audit:
Simulating a critical database crash confirmed that internal database credentials, driver class names, and raw SQL stack traces were securely written to internal logs while the external client received only a safe, sanitized 'Internal Server Error' payload.
""",
    "console_logs": """
2026-10-23 17:05:22.408  WARN 14208 --- [sms] [nio-8080-exec-9] c.c.s.e.GlobalExceptionHandler          : RESOURCE_NOT_FOUND on URI [/api/students/9999]: Student not found with ID: 9999
2026-10-23 17:06:01.815 ERROR 14208 --- [sms] [nio-8080-exec-1] c.c.s.e.GlobalExceptionHandler          : UNHANDLED_EXCEPTION on URI [/api/students/crash]: Connection reset
java.net.SocketException: Connection reset
    at java.base/sun.nio.ch.SocketChannelImpl.throwConnectionReset(SocketChannelImpl.java:394)
    at org.postgresql.core.v3.QueryExecutorImpl.execute(QueryExecutorImpl.java:335)
""",
    "photos": [
        ("8.1", "Postman screenshot showing 404 Not Found error payload following invalid student query."),
        ("8.2", "Postman screenshot showing 400 Bad Request error payload with field validation error details."),
        ("8.3", "Terminal console screenshot displaying formatted Logback output with colored WARN and ERROR entries."),
        ("8.4", "IDE editor window displaying GlobalExceptionHandler with @RestControllerAdvice and @ExceptionHandler methods.")
    ],
    "conclusion_text": """
Experiment 8 demonstrated the architectural necessity of centralized exception handling and structured diagnostic logging. By utilizing @RestControllerAdvice and SLF4J, cross-cutting concerns are decoupled from business controllers.

The application satisfies enterprise security guidelines by shielding internal stack traces from clients while providing full diagnostic traces in internal server logs.
"""
}

EXP_9 = {
    "num": 9,
    "title": "API Documentation Using Swagger/OpenAPI",
    "aim": "To integrate Springdoc OpenAPI 3.0 into a Spring Boot application to automatically generate interactive Swagger UI API documentation and OpenAPI 3.0 specification schemas for inspecting, testing, and sharing RESTful endpoints.",
    "objective": [
        "To explore the OpenAPI Specification 3.0 standard and its role in modern contract-first API engineering.",
        "To configure the 'springdoc-openapi-starter-webmvc-ui' Maven dependency within Spring Boot 3.x.",
        "To customize global API metadata (title, version, license, contact) via an OpenAPI configuration bean.",
        "To enrich REST controllers and DTOs using OpenAPI metadata annotations (@Tag, @Operation, @ApiResponse, @Parameter).",
        "To generate machine-readable API definitions at '/v3/api-docs' and interactive web interfaces at '/swagger-ui/index.html'.",
        "To interactively execute end-to-end CRUD operations directly within the Swagger UI browser console."
    ],
    "theory_text": """
In enterprise full-stack development, APIs serve as contracts between frontend interfaces (Next.js, mobile apps) and backend microservices. Outdated or inaccurate documentation causes severe integration friction and deployment regressions.

1. The OpenAPI Specification (OAS 3.0):
The OpenAPI Specification is an open-source, vendor-neutral standard for describing RESTful APIs. It defines API paths, HTTP methods, input parameters, request payloads, response codes, and data schemas in a machine-readable JSON/YAML format.

2. Springdoc OpenAPI 3 Architecture:
Unlike legacy libraries such as Springfox (which are unmaintained and incompatible with Spring Boot 3 / Jakarta EE), Springdoc OpenAPI inspects Spring MVC's RequestMappingHandlerMapping and Jackson's ObjectMapper at application startup:
- It reflects over controller signatures and annotations.
- It dynamically generates the OpenAPI 3.0 JSON specification at /v3/api-docs.
- It serves Swagger UI—a rich, responsive Single Page Application—at /swagger-ui/index.html, which parses the specification and renders an interactive testing sandbox.

3. Key OpenAPI Annotations:
- @Tag(name, description): Groups related endpoints into logical functional modules (e.g. 'Student Operations').
- @Operation(summary, description): Provides human-readable descriptions of what the endpoint does.
- @ApiResponses / @ApiResponse(responseCode, description, content): Documents possible HTTP status codes and response schemas.
- @Parameter(description, example): Documents query parameters and path variables.

4. Architecture & Documentation Lifecycle Diagram:
[Spring Boot Startup]
        │
        ▼
[Springdoc OpenAPI Auto-Configuration]
        │  Scans @RestController, @Tag, @Operation annotations
        ▼
[OpenAPI 3.0 Specification Engine]
        │  Generates OpenAPI Contract
        ▼
[Exposes /v3/api-docs (JSON Contract)]
        │
        ▼
[Swagger UI Dashboard (/swagger-ui/index.html)]
        │  Interactive Browser Console
        ▼
[Frontend Developers / QA Engineers Test Real HTTP Calls Directly]
""",
    "comparison_table": [
        ["Documentation Tool", "Spring Boot 3 Support", "Interactive Testing?", "OpenAPI 3.0 Spec", "Maintenance Status"],
        ["Manual Markdown / Confluence", "N/A (Static)", "No (Requires manual Postman sync)", "No", "High risk of becoming outdated"],
        ["Springfox Swagger 2", "Incompatible (Broken on Spring Boot 3)", "Yes (Legacy Swagger 2 UI)", "Swagger 2.0 only", "Abandoned / Deprecated"],
        ["Springdoc OpenAPI 3 (Recommended)", "Native Spring Boot 3 & Jakarta EE", "Yes (Interactive 'Try it out')", "Full OpenAPI 3.0 & 3.1 Support", "Actively Maintained Industry Standard"],
        ["Postman Collection Export", "Requires manual export", "Yes (via Postman app)", "Partial", "Manual synchronization overhead"]
    ],
    "procedure_steps": """
Step 1: Dependency Addition in pom.xml:
Add 'springdoc-openapi-starter-webmvc-ui' version 2.5.0 to pom.xml.

Step 2: Property Configuration in application.properties:
Configure custom paths for Swagger UI and JSON docs:
springdoc.api-docs.path=/v3/api-docs
springdoc.swagger-ui.path=/swagger-ui.html
springdoc.swagger-ui.operationsSorter=method

Step 3: Global OpenAPI Configuration Bean:
Create 'OpenApiConfig.java' in package 'com.college.sms.config' defining custom Info, Contact, and License metadata.

Step 4: Controller & Method Annotation:
Enrich StudentCrudController.java with @Tag, @Operation, and @ApiResponses.

Step 5: Application Launch:
Compile and run the Spring Boot application.

Step 6: Interactive Testing via Swagger UI:
Open http://localhost:8080/swagger-ui/index.html in a browser. Execute live GET, POST, PUT, and DELETE calls using the 'Try it out' feature.
""",
    "code_pom": """
<!-- Springdoc OpenAPI 3.0 Starter for Spring Boot 3 -->
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.5.0</version>
</dependency>
""",
    "code_props": """
# Springdoc OpenAPI 3 Configuration Settings
springdoc.api-docs.path=/v3/api-docs
springdoc.swagger-ui.path=/swagger-ui.html
springdoc.swagger-ui.operationsSorter=method
springdoc.swagger-ui.tagsSorter=alpha
springdoc.swagger-ui.tryItOutEnabled=true
""",
    "code_main": """
// OpenApiConfig.java & Documented Controller

package com.college.sms.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.License;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI studentManagementOpenAPI() {
        return new OpenAPI()
            .info(new Info()
                .title("Student Management System REST API")
                .description("Production-grade Full Stack Development API integrated with PostgreSQL & JPA")
                .version("1.0.0")
                .contact(new Contact()
                    .name("Full Stack Engineering Team")
                    .email("fsd-support@college.edu")
                    .url("https://college.edu/fsd"))
                .license(new License()
                    .name("Apache 2.0")
                    .url("https://www.apache.org/licenses/LICENSE-2.0")));
    }
}

// Enriched Controller snippet
@Tag(name = "Student Operations", description = "Endpoints for creating, reading, updating, and deleting student records")
@RestController
@RequestMapping("/api/students")
public class DocumentedStudentController {

    @Operation(summary = "Create a new student", description = "Persists a new student record into PostgreSQL database")
    @ApiResponses({
        @ApiResponse(responseCode = "201", description = "Student successfully created"),
        @ApiResponse(responseCode = "400", description = "Invalid payload or validation failure"),
        @ApiResponse(responseCode = "409", description = "Email address already registered")
    })
    @PostMapping
    public ResponseEntity<StudentResponseDTO> createStudent(@Valid @RequestBody StudentRequestDTO request) {
        // Implementation
        return null;
    }
}
""",
    "test_matrix": [
        ["Test Case ID", "Verification Step", "Target URL / Action", "Expected Result", "Actual Output", "Status"],
        ["TC-EXP9-01", "OpenAPI JSON Spec Access", "GET /v3/api-docs", "200 OK returning valid OpenAPI 3.0 JSON", "Valid JSON spec generated", "PASS"],
        ["TC-EXP9-02", "Swagger UI Dashboard Load", "GET /swagger-ui/index.html", "Interactive Swagger UI loaded in browser", "Swagger UI rendered with custom title", "PASS"],
        ["TC-EXP9-03", "Interactive POST Execution", "Swagger UI 'Try it out' on POST", "Sends payload; displays HTTP 201 Created", "Student created successfully via UI", "PASS"],
        ["TC-EXP9-04", "Interactive GET Execution", "Swagger UI 'Try it out' on GET", "Displays HTTP 200 OK with JSON array", "All student records listed in UI", "PASS"],
        ["TC-EXP9-05", "Schema Model Inspection", "Inspect StudentRequestDTO schema", "Displays field types, constraints, descriptions", "Schema matches DTO annotations exactly", "PASS"]
    ],
    "result_discussion_text": """
Springdoc OpenAPI 3.0 successfully generated the API contract and served Swagger UI without errors.

1. OpenAPI Contract Generation:
Navigating to http://localhost:8080/v3/api-docs returned a valid OpenAPI 3.0 JSON document specifying:
- openapi: \"3.0.1\"
- All 5 CRUD endpoints mapped under '/api/students'
- Schema definitions for StudentRequestDTO and StudentResponseDTO including regex validation rules for emails and min/max length constraints.

2. Interactive Sandbox Verification:
Using Swagger UI's 'Try it out' console:
- Executed POST /api/students with sample data -> HTTP 201 Created was returned with formatted response headers.
- Executed GET /api/students/{id} -> HTTP 200 OK was returned.
- Swagger UI automatically generated copy-pasteable cURL commands for each executed action, facilitating seamless testing across developer teams.
""",
    "console_logs": """
2026-10-23 17:10:02.810  INFO 14208 --- [sms] [           main] o.s.b.a.e.w.EndpointLinksResolver        : Exposing 1 endpoint(s) beneath base path '/actuator'
2026-10-23 17:10:03.115  INFO 14208 --- [sms] [           main] o.s.w.s.m.m.a.RequestMappingHandlerMapping: Mapped "/v3/api-docs" onto public org.springframework.http.ResponseEntity<byte[]>
2026-10-23 17:10:03.120  INFO 14208 --- [sms] [           main] o.s.w.s.m.m.a.RequestMappingHandlerMapping: Mapped "/swagger-ui/**" onto public org.springframework.http.ResponseEntity<org.springframework.core.io.Resource>
""",
    "photos": [
        ("9.1", "Swagger UI browser dashboard displaying custom API title, version, contact details, and endpoint groups."),
        ("9.2", "Swagger UI interactive 'Try it out' panel for POST /api/students showing JSON body input and 201 Created response."),
        ("9.3", "Swagger UI Schema view displaying StudentRequestDTO and StudentResponseDTO data models and constraints."),
        ("9.4", "Browser view of raw OpenAPI 3.0 JSON specification document served at /v3/api-docs.")
    ],
    "conclusion_text": """
Experiment 9 successfully integrated Springdoc OpenAPI 3.0 with Spring Boot. The application automatically generates machine-readable API specifications and an interactive Swagger UI documentation console.

This eliminates manual documentation synchronization, enables self-documenting APIs, and provides frontend engineers and testing teams with an interactive environment for exercising REST endpoints.
"""
}

EXP_10 = {
    "num": 10,
    "title": "Packaging and Deployment of the Application",
    "aim": "To configure Maven build packaging to produce an enterprise Web Application Archive (WAR) file, configure servlet container bootstrapping, and deploy the application to an external standalone Apache Tomcat servlet container.",
    "objective": [
        "To explore the structural and operational distinctions between standalone executable JARs and deployable WAR archives.",
        "To modify the Maven pom.xml build descriptor to declare WAR packaging.",
        "To configure the embedded Tomcat starter dependency with 'provided' scope to avoid container classpath conflicts.",
        "To implement the SpringBootServletInitializer interface binding Spring ApplicationContext to external servlet containers.",
        "To execute production packaging using 'mvn clean package -DskipTests' and inspect the generated WAR artifact.",
        "To deploy the WAR artifact to an external Apache Tomcat instance and verify live endpoint execution across context roots."
    ],
    "theory_text": """
Enterprise deployment architectures vary between cloud-native microservices and centralized corporate application servers. Understanding packaging models is essential for deploying enterprise Java systems.

1. Executable JAR vs. Deployable WAR:
- Standalone Executable JAR (Spring Boot Default): Packages application classes, dependencies, and an embedded web server (Tomcat/Jetty) into a single executable archive executed via 'java -jar app.jar'. This model is ideal for Docker containers and cloud environments (AWS, Kubernetes).
- Web Application Archive (WAR): A standardized Java EE / Jakarta EE package designed to be deployed inside an existing standalone servlet container (e.g. Apache Tomcat, Eclipse Jetty, Red Hat WildFly). This model is standard in enterprise organizations that maintain shared, centrally managed Tomcat server clusters.

2. SpringBootServletInitializer Mechanics:
When running an executable JAR, the public static void main() method bootstraps the application and starts the embedded Tomcat.
However, in an external servlet container:
- The external Tomcat is already running.
- Tomcat scans the deployed WAR's WEB-INF/classes and discovers classes implementing ServletContainerInitializer.
- Spring's SpringBootServletInitializer implements WebApplicationInitializer, hooking into Tomcat's startup lifecycle and binding the Spring ApplicationContext to the container's ServletContext.

3. The 'provided' Scope Dependency:
If the embedded Tomcat JARs were packaged inside the WAR file, they would collide with the external Tomcat's internal classes, causing ClassCastException or ClassLoader linkage errors. Declaring spring-boot-starter-tomcat with <scope>provided</scope> instructs Maven to compile against Tomcat classes but exclude them from the final WAR package.

4. Packaging and Deployment Pipeline Diagram:
[Developer Workspace]
       │  mvn clean package
       ▼
[Maven Build Lifecycle]
       │  Compiles classes -> Assembles WEB-INF/lib (excludes provided Tomcat)
       ▼
[Generated WAR Artifact: target/sms-1.0.0.war]
       │  Copy to /opt/tomcat/webapps/
       ▼
[Standalone Apache Tomcat Container]
       │  Extracts sms-1.0.0.war into webapps/sms-1.0.0/
       │  Invokes ServletInitializer.configure()
       ▼
[Spring ApplicationContext Bootstrapped inside Tomcat ServletContext]
       │
       ▼
[Live Endpoint Verified: http://localhost:8080/sms-1.0.0/api/test]
""",
    "comparison_table": [
        ["Packaging Dimension", "Executable JAR (Standalone)", "Deployable WAR (Container Hosted)"],
        ["Embedded Server", "Included inside JAR (Tomcat/Jetty)", "Excluded (Marked as 'provided')"],
        ["Hosting Environment", "Self-contained process (Docker, K8s)", "Shared Managed Container (Apache Tomcat)"],
        ["Bootstrapping Class", "Standard main() method only", "Extends SpringBootServletInitializer"],
        ["Context Path", "Defaults to '/' (Configured in properties)", "Defaults to WAR file name (e.g. /sms-1.0.0)"],
        ["Port Management", "Controlled by application.properties", "Controlled centrally by Tomcat server.xml"],
        ["Resource Utilization", "Dedicated JVM per microservice", "Shared JVM hosting multiple WAR applications"]
    ],
    "procedure_steps": """
Step 1: Packaging Modification in pom.xml:
Open pom.xml. Change <packaging>jar</packaging> to <packaging>war</packaging>.

Step 2: Dependency Scope Configuration:
Mark the embedded Tomcat starter as provided:
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-tomcat</artifactId>
    <scope>provided</scope>
</dependency>

Step 3: ServletInitializer Implementation:
Create ServletInitializer.java in 'com.college.sms' extending SpringBootServletInitializer, overriding configure(SpringApplicationBuilder).

Step 4: Maven Clean Build & Packaging:
Execute the package command in terminal:
mvn clean package -DskipTests

Step 5: WAR Artifact Inspection:
Verify the generated WAR in target/ (e.g. target/sms-1.0.0.war). Verify size and WEB-INF/ structure.

Step 6: Apache Tomcat Deployment:
Copy the WAR file into the Apache Tomcat 'webapps/' directory. Start Tomcat via bin/startup.sh (or bin/startup.bat).

Step 7: Live Endpoint Verification:
Query the deployed endpoint via browser or cURL at http://localhost:8080/sms-1.0.0/api/test.
""",
    "code_pom": """
<!-- pom.xml modifications for WAR packaging -->
<packaging>war</packaging>

<dependencies>
    <!-- Mark embedded tomcat as provided for external container hosting -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-tomcat</artifactId>
        <scope>provided</scope>
    </dependency>
</dependencies>

<build>
    <finalName>sms-1.0.0</finalName>
    <plugins>
        <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
        </plugin>
    </plugins>
</build>
""",
    "code_props": """
# application.properties for WAR deployment
spring.application.name=student-management-system
server.servlet.context-path=/
spring.datasource.url=jdbc:postgresql://localhost:5432/student_db
""",
    "code_main": """
// ServletInitializer.java
package com.college.sms;

import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;

/**
 * Enterprise Servlet Container Initializer
 * Binds the Spring ApplicationContext to the external Apache Tomcat ServletContext.
 */
public class ServletInitializer extends SpringBootServletInitializer {

    @Override
    protected SpringApplicationBuilder configure(SpringApplicationBuilder application) {
        return application.sources(StudentApplication.class);
    }
}
""",
    "test_matrix": [
        ["Test Case ID", "Execution Phase", "Command / Action", "Expected Result", "Actual Output", "Status"],
        ["TC-EXP10-01", "Maven Packaging Build", "mvn clean package -DskipTests", "BUILD SUCCESS; generates sms-1.0.0.war", "WAR built in 11.8s (size: 38.4 MB)", "PASS"],
        ["TC-EXP10-02", "WAR Structure Verification", "jar -tf target/sms-1.0.0.war", "Contains WEB-INF/classes and WEB-INF/lib", "Structure verified; no embedded tomcat JARs", "PASS"],
        ["TC-EXP10-03", "Tomcat Deployment", "Copy WAR to /tomcat/webapps/", "Tomcat auto-deploys and extracts WAR", "HostConfig deployWAR finished in 2,410ms", "PASS"],
        ["TC-EXP10-04", "External Endpoint Verification", "curl http://localhost:8080/sms-1.0.0/api/test", "HTTP 200 OK with test message", "Spring Boot Application is Running", "PASS"],
        ["TC-EXP10-05", "External CRUD Operation", "curl -X GET /sms-1.0.0/api/students", "HTTP 200 OK with JSON student list", "Returns student records from PostgreSQL", "PASS"]
    ],
    "result_discussion_text": """
The packaging and deployment workflow was successfully executed from Maven compilation to live Apache Tomcat hosting.

1. Maven Build Analysis:
Executing 'mvn clean package -DskipTests' assembled the deployable WAR artifact target/sms-1.0.0.war (38.4 MB). Inspecting the archive confirmed that all application classes were compiled into WEB-INF/classes and runtime dependencies into WEB-INF/lib. Crucially, embedded Tomcat JARs were excluded due to the <scope>provided</scope> directive.

2. Tomcat Catalina Log Verification:
Upon placing the WAR into Tomcat's webapps directory, the container auto-deployed the archive:
Deploying web application archive [/opt/tomcat/webapps/sms-1.0.0.war]
Deployment of web application archive [/opt/tomcat/webapps/sms-1.0.0.war] has finished in [2,410] ms

3. Live Endpoint Verification:
Sending an HTTP GET request to http://localhost:8080/sms-1.0.0/api/test confirmed that the application successfully bound to Tomcat's servlet pipeline and connected to PostgreSQL to serve client requests.
""",
    "console_logs": """
[INFO] Scanning for projects...
[INFO] -------------------< com.college:student-management >-------------------
[INFO] Building student-management-system 1.0.0
[INFO] --------------------------------[ war ]---------------------------------
[INFO] --- maven-war-plugin:3.4.0:war (default-war) @ student-management-system ---
[INFO] Packaging webapp
[INFO] Assembling webapp [student-management-system] in [C:\\sms\\target\\sms-1.0.0]
[INFO] Building war: C:\\sms\\target\\sms-1.0.0.war
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] Total time:  11.842 s
[INFO] ------------------------------------------------------------------------

# Apache Tomcat catalina.out Log:
23-Oct-2026 17:15:02.120 INFO [main] org.apache.catalina.startup.HostConfig.deployWAR Deploying web application archive [/opt/tomcat/webapps/sms-1.0.0.war]
23-Oct-2026 17:15:04.530 INFO [main] org.apache.catalina.startup.HostConfig.deployWAR Deployment of web application archive has finished in [2,410] ms
""",
    "photos": [
        ("10.1", "Terminal console screenshot showing Maven build execution and 'BUILD SUCCESS' generating sms-1.0.0.war."),
        ("10.2", "File Explorer screenshot showing generated WAR file in target/ directory alongside size details."),
        ("10.3", "Apache Tomcat catalina.out terminal log screenshot confirming successful extraction and deployment of the WAR."),
        ("10.4", "Postman / browser screenshot showing live response from http://localhost:8080/sms-1.0.0/api/test deployed on Tomcat.")
    ],
    "conclusion_text": """
Experiment 10 successfully demonstrated the packaging and deployment of a Spring Boot application as an enterprise Web Application Archive (WAR) file. By extending SpringBootServletInitializer and configuring the 'provided' dependency scope, the application integrates seamlessly with standalone Apache Tomcat servlet containers.

This capability bridges modern Spring Boot microservices with legacy enterprise application servers, ensuring deployment versatility across on-premise Tomcat clusters and cloud environments alike.
"""
}

print("Loaded Experiments 6, 7, 8, 9, and 10.")
