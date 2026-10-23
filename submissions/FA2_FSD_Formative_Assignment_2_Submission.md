# FULL STACK DEVELOPMENT - I (PS-FSD)
## FORMATIVE ASSIGNMENT - 2 (FA-2)
**Academic Year:** 2026-27 | **Semester:** V  
**Max Marks:** 20 | **Subject Code:** FSD-1  

---

### Question Overview Table

| Q. No. | Question Focus | Bloom's Level | Marks |
|---|---|---|---|
| **1** | ORM Technology Selection & Demonstration in Student Management System | L3 – Apply | 4 |
| **2** | PostgreSQL Suitability Analysis for E-Commerce Consistency & Relations | L4 – Analyze | 4 |
| **3** | Spring Boot REST API: `@Controller` vs `@RestController` & JSON Retrieval | L4 – Analyze, L6 – Create | 4 |
| **4** | Production SLF4J Diagnostic Logging for Student API Failures | L4 – Analyze, L6 – Create | 4 |
| **5** | Interactive API Documentation with Springdoc OpenAPI / Swagger UI | L3 – Apply, L6 – Create | 4 |

---

### Question 1: ORM Technology Selection & Demonstration
**Question:** *A college is developing a Student Management System using Spring Boot and PostgreSQL. The developer wants to store student objects in the database without writing SQL queries for every operation. Identify a suitable ORM technology and demonstrate how it simplifies database interactions using an appropriate example. (4 Marks, L3 - Apply)*

#### 1. Identification:
The recommended ORM technology is **Spring Data JPA** with **Hibernate** as the JPA persistence provider.

#### 2. Key Advantages:
1. **Automated CRUD & Query Derivation:** `JpaRepository<T, ID>` provides `save()`, `findById()`, `findAll()`, and `deleteById()` out-of-the-box. Custom queries are automatically generated from method names (e.g. `findByDepartment(String dept)`).
2. **Elimination of JDBC Boilerplate:** Eliminates manual `DriverManager` connections, `PreparedStatement` parameter bindings, `ResultSet` column mapping, and manual resource cleanup (`try-with-resources`).
3. **Dirty Checking & Unit of Work:** Modifying an entity inside a `@Transactional` boundary automatically synchronizes updates to PostgreSQL during flush/commit without explicit `UPDATE` statements.

#### 3. Code Demonstration:
```java
// 1. Entity Definition
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

    @Column(nullable = false, length = 50)
    private String department;
}

// 2. Repository Interface (Zero SQL written)
package com.college.sms.repository;
import com.college.sms.entity.Student;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface StudentRepository extends JpaRepository<Student, Long> {
}

// 3. Service Layer Demonstrating Simplified Persistence
@Service
@Transactional
public class StudentService {
    private final StudentRepository repository;

    public StudentService(StudentRepository repository) {
        this.repository = repository;
    }

    public Student saveStudent(Student student) {
        // Automatically issues: INSERT INTO students (name, email, department) VALUES (?, ?, ?)
        return repository.save(student);
    }
}
```

---

### Question 2: PostgreSQL Suitability for E-Commerce Applications
**Question:** *An e-commerce application stores customer details, product information, and orders in PostgreSQL. The application frequently retrieves related records and must maintain data consistency. Analyze why PostgreSQL is suitable for this application and justify your answer with relevant database features. (4 Marks, L4 - Analyze)*

#### Architectural Analysis & Feature Justification:
1. **Strict ACID Compliance & Transactional Integrity:**  
   In e-commerce, checking out an order involves creating an order record, decrementing inventory stock, and charging a payment card. PostgreSQL ensures **Atomicity** and **Isolation** so that either all three actions succeed or the transaction rolls back completely, preventing inventory overselling.
2. **Multi-Version Concurrency Control (MVCC):**  
   PostgreSQL uses MVCC so readers do not lock out writers and writers do not block readers. Thousands of users browsing product pages and reading catalogs will not lock tables or degrade performance for users confirming orders.
3. **Native JSONB with GIN Indexing:**  
   E-commerce products have dynamic attributes (e.g., sizes, color variations, tech specifications) that vary wildly across categories. PostgreSQL's native `JSONB` data type stores structured JSON with indexing via Generalized Inverted Indexes (GIN), enabling sub-millisecond filtering on nested product attributes without sparse column proliferation.
4. **Declarative Foreign Keys with Referential Cascading:**  
   Enforces relational integrity between `Customers`, `Orders`, and `Order_Items`. Deleting or updating a record adheres to explicit business rules (`ON DELETE CASCADE` or `RESTRICT`), preventing orphaned order line items.
5. **Row-Level Locking (`SELECT ... FOR UPDATE`):**  
   Provides precise concurrency control during high-traffic flash sales to lock only the specific product inventory row while reserving stock, preventing race conditions.

---

### Question 3: `@Controller` vs `@RestController` & JSON REST Endpoint
**Question:** *A developer needs to build a Spring Boot REST API that returns student details in JSON format when a client sends a GET request. Analyze the suitability of @Controller and @RestController, select the appropriate annotation, and create a sample controller method to retrieve student details. (4 Marks, L4 - Analyze, L6 - Create)*

#### 1. Comparative Analysis:
- **`@Controller`:** Designed for traditional Spring MVC server-side template rendering (Thymeleaf, JSP). Method return values are interpreted as view names unless explicitly annotated with `@ResponseBody` on every single method.
- **`@RestController`:** A specialized meta-annotation composed of `@Controller + @ResponseBody`. It instructs Spring's `HttpMessageConverter` (Jackson) to serialize return values directly into the HTTP response body as JSON.

**Selection:** `@RestController` is the clear choice for REST APIs serving single-page apps (React/Next.js), mobile clients, or microservices.

#### 2. Sample REST Controller Implementation:
```java
package com.college.sms.controller;

import com.college.sms.entity.Student;
import com.college.sms.repository.StudentRepository;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

@RestController
@RequestMapping("/api/students")
public class StudentController {

    private final StudentRepository studentRepository;

    public StudentController(StudentRepository studentRepository) {
        this.studentRepository = studentRepository;
    }

    /**
     * GET /api/students/{id}
     * Returns student record as JSON payload with HTTP 200 OK or HTTP 404 Not Found
     */
    @GetMapping(value = "/{id}", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Student> getStudentById(@PathVariable Long id) {
        Student student = studentRepository.findById(id)
            .orElseThrow(() -> new ResponseStatusException(
                HttpStatus.NOT_FOUND, 
                "Student not found with ID: " + id
            ));

        return ResponseEntity.ok(student);
    }
}
```

---

### Question 4: Diagnostic Logging & SLF4J Statements
**Question:** *A Student Management API occasionally fails while retrieving student records. The development team needs meaningful logs to identify failed operations and troubleshoot errors. Analyze the information that should be recorded and write suitable SLF4J Logger statements to log the student ID, operation, and exception details. (4 Marks, L4 - Analyze, L6 - Create)*

#### 1. Diagnostic Information Analysis:
To diagnose failures in production without leaking personally identifiable information (PII), the logger must record:
- **Operation Name & Context:** E.g., `FETCH_STUDENT_BY_ID`.
- **Target Entity Identifier:** The requested `studentId`.
- **Appropriate Log Level:**
  - `INFO`: Entry and successful completion of critical operations.
  - `WARN`: Expected business exceptions (e.g. record not found for given ID).
  - `ERROR`: Unhandled system anomalies (e.g. database connection dropped, SQL timeout) accompanied by the complete `Throwable` stack trace.
- **Timestamp & Thread/Trace ID:** Managed automatically by Logback / SLF4J pattern configuration.

#### 2. Implementation with SLF4J Statements:
```java
package com.college.sms.service;

import com.college.sms.entity.Student;
import com.college.sms.repository.StudentRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

@Service
public class StudentService {

    private static final Logger log = LoggerFactory.getLogger(StudentService.class);
    private final StudentRepository studentRepository;

    public StudentService(StudentRepository studentRepository) {
        this.studentRepository = studentRepository;
    }

    public Student getStudentDetails(Long studentId) {
        final String operation = "FETCH_STUDENT_BY_ID";
        
        // Log operation initiation with parameterization
        log.info("Initiating operation [{}] for student ID: {}", operation, studentId);

        try {
            return studentRepository.findById(studentId)
                .orElseThrow(() -> {
                    // Log warning when student ID is absent in database
                    log.warn("Operation [{}] failed - Student not found for ID: {}", operation, studentId);
                    return new RuntimeException("Student not found for ID: " + studentId);
                });
        } catch (Exception ex) {
            // Log error with operation name, student ID, error message, AND the exception stack trace
            log.error("Operation [{}] encountered critical error while retrieving student ID: {}. Reason: {}",
                      operation, studentId, ex.getMessage(), ex);
            throw ex;
        }
    }
}
```

---

### Question 5: Interactive API Documentation (Springdoc OpenAPI / Swagger UI)
**Question:** *A development team has implemented REST APIs for adding, retrieving, updating, and deleting student records. The testing team needs interactive API documentation to inspect endpoints, provide request parameters, and test responses. Select a suitable documentation tool and design the steps required to integrate it with Spring Boot and test the APIs. (4 Marks, L3 - Apply, L6 - Create)*

#### 1. Tool Selection:
The standard tool for modern Spring Boot applications is **Springdoc OpenAPI 3** (`springdoc-openapi-starter-webmvc-ui`), which generates interactive Swagger UI matching the OpenAPI 3.0 specification.

#### 2. Integration Steps:

**Step 1: Add Dependency to `pom.xml`**
```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.5.0</version>
</dependency>
```

**Step 2: Configure Properties in `application.properties`**
```properties
springdoc.api-docs.path=/v3/api-docs
springdoc.swagger-ui.path=/swagger-ui.html
springdoc.swagger-ui.operationsSorter=method
```

**Step 3: Enrich Controller with Swagger Annotations**
```java
package com.college.sms.controller;

import com.college.sms.entity.Student;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/students")
@Tag(name = "Student Operations", description = "CRUD endpoints for managing student records")
public class StudentDocController {

    @Operation(summary = "Create Student", description = "Adds a new student to PostgreSQL")
    @ApiResponse(responseCode = "201", description = "Student created successfully")
    @PostMapping
    public ResponseEntity<Student> createStudent(@RequestBody Student student) {
        return new ResponseEntity<>(student, HttpStatus.CREATED);
    }

    @Operation(summary = "Get Student by ID", description = "Retrieves student record by primary key ID")
    @ApiResponse(responseCode = "200", description = "Student found")
    @ApiResponse(responseCode = "404", description = "Student ID does not exist")
    @GetMapping("/{id}")
    public ResponseEntity<Student> getStudentById(@PathVariable Long id) {
        return ResponseEntity.ok(new Student());
    }
}
```

#### 3. Testing Workflow via Swagger UI:
1. Start the Spring Boot application and open `http://localhost:8080/swagger-ui/index.html`.
2. Inspect the interactive visual listing of all endpoints categorized under `Student Operations`.
3. Click on any endpoint (e.g. `POST /api/students`), click **"Try it out"**, fill in the JSON body, and click **"Execute"**.
4. Review the real-time HTTP response code (201 Created), response headers, and JSON body.
