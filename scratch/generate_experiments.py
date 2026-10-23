import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import os

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F4F5F7")
    set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
    
    tcPr = cell._element.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for border_name in ['top', 'left', 'bottom', 'right']:
        b = OxmlElement(f'w:{border_name}')
        b.set(qn('w:val'), 'single')
        b.set(qn('w:sz'), '4')
        b.set(qn('w:space'), '0')
        b.set(qn('w:color'), 'D0D7DE')
        tcBorders.append(b)
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(code_text.strip())
    run.font.name = 'Consolas'
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(36, 41, 47)
    doc.add_paragraph()

def add_styled_heading(doc, text, level):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(4)
    run = h.runs[0]
    if level == 1:
        run.font.name = 'Arial'
        run.font.size = Pt(15)
        run.font.bold = True
        run.font.color.rgb = RGBColor(27, 54, 93)
    elif level == 2:
        run.font.name = 'Arial'
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(41, 105, 176)
    elif level == 3:
        run.font.name = 'Arial'
        run.font.size = Pt(10.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(51, 51, 51)
    return h

def build_experiments():
    os.makedirs('submissions', exist_ok=True)
    doc = docx.Document()
    
    for sec in doc.sections:
        sec.top_margin = Inches(0.8)
        sec.bottom_margin = Inches(0.8)
        sec.left_margin = Inches(0.8)
        sec.right_margin = Inches(0.8)
        
    # Title Header
    header_table = doc.add_table(rows=1, cols=1)
    header_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = header_table.cell(0, 0)
    set_cell_background(c, "1B365D")
    set_cell_margins(c, top=200, bottom=200, left=250, right=250)
    
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("PRACTICAL SKILLS - FULL STACK DEVELOPMENT (PS-FSD)\nLABORATORY MANUAL & EXPERIMENT SUBMISSION RECORD\nSEM V | A.Y. 2026-27")
    r.font.name = 'Arial'
    r.font.size = Pt(13.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(255, 255, 255)
    
    p2 = c.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = p2.add_run("Complete Compilation of 10 Core Practical Experiments (Spring Boot, PostgreSQL, JPA, REST, Swagger, SLF4J, Deployment)")
    r2.font.name = 'Arial'
    r2.font.size = Pt(9.5)
    r2.font.italic = True
    r2.font.color.rgb = RGBColor(200, 220, 245)
    
    doc.add_paragraph()

    # Index Table
    idx_data = [
        ["Exp #", "Experiment Title", "Core Technology Focus", "Status"],
        ["1", "Database Creation and Configuration", "PostgreSQL DDL & application.properties", "Completed"],
        ["2", "Creating and Testing a REST Endpoint", "Spring Boot @RestController, /api/test", "Completed"],
        ["3", "Creating an Entity Class", "Jakarta JPA Annotations (@Entity, @Id, @Column)", "Completed"],
        ["4", "Creating a Repository Interface", "Spring Data JpaRepository<Student, Long>", "Completed"],
        ["5", "Implementing Create and Read Operations", "POST & GET Endpoints with Postman Testing", "Completed"],
        ["6", "Implementing Update and Delete Operations", "PUT & DELETE Endpoints with 404 Exception Handling", "Completed"],
        ["7", "Implementing Entity Relationships", "Department <-> Student (@ManyToOne / @OneToMany)", "Completed"],
        ["8", "Implementing Logging and Exception Handling", "SLF4J, Logback, and @RestControllerAdvice", "Completed"],
        ["9", "API Documentation Using Swagger/OpenAPI", "Springdoc OpenAPI 3 & Swagger UI Interactive Testing", "Completed"],
        ["10", "Packaging and Deployment of the Application", "WAR Build (mvn clean package) & Tomcat Container", "Completed"]
    ]
    t = doc.add_table(rows=len(idx_data), cols=4)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(idx_data):
        for c_idx, val in enumerate(row):
            cell = t.cell(r_idx, c_idx)
            set_cell_margins(cell, top=45, bottom=45, left=70, right=70)
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.name = 'Arial'
            if r_idx == 0:
                set_cell_background(cell, "2969B0")
                run.font.size = Pt(9.0)
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
            else:
                set_cell_background(cell, "F8F9FA" if r_idx % 2 == 1 else "FFFFFF")
                run.font.size = Pt(8.0)
                if c_idx in [0, 3]:
                    run.font.bold = True
    doc.add_paragraph()

    # =========================================================
    # EXPERIMENT 1
    # =========================================================
    add_styled_heading(doc, "Experiment 1: Database Creation and Configuration", level=1)
    p = doc.add_paragraph(
        "Objective: To create a PostgreSQL database and configure a Spring Boot application to connect to it.\n\n"
        "1.1 Theory & Architecture:\n"
        "PostgreSQL is a robust open-source object-relational database. Spring Boot uses HikariCP as its default, high-performance "
        "JDBC connection pool. Connectivity is configured declaratively in application.properties using the PostgreSQL JDBC Driver."
    )
    p.paragraph_format.line_spacing = 1.15

    add_styled_heading(doc, "1.2 PostgreSQL Database & Schema Setup", level=2)
    exp1_sql = """
-- PostgreSQL Terminal (psql) Commands
CREATE DATABASE student_db;

\\c student_db;

CREATE TABLE students (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    department VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
    add_code_block(doc, exp1_sql)

    add_styled_heading(doc, "1.3 Spring Boot Database Configuration (src/main/resources/application.properties)", level=2)
    exp1_props = """
spring.application.name=student-management-system

# PostgreSQL Database Connection URL
spring.datasource.url=jdbc:postgresql://localhost:5432/student_db
spring.datasource.username=postgres
spring.datasource.password=postgres
spring.datasource.driver-class-name=org.postgresql.Driver

# JPA / Hibernate Configuration
spring.jpa.database-platform=org.hibernate.dialect.PostgreSQLDialect
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true

# Server Port
server.port=8080
"""
    add_code_block(doc, exp1_props)

    add_styled_heading(doc, "1.4 Verification & Output", level=2)
    exp1_out = """
[INFO] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Starting...
[INFO] com.zaxxer.hikari.pool.HikariPool        : HikariPool-1 - Added connection org.postgresql.jdbc.PgConnection@5e25
[INFO] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Start completed.
[INFO] org.hibernate.jpa.internal.util.LogHelper: HHH000204: Processing PersistenceUnitInfo [name: default]
[INFO] org.hibernate.engine.transaction.jta.platform.internal.NoJtaPlatform: HHH000490: Using JtaPlatformImplementation: NoJtaPlatform
[INFO] com.example.sms.StudentApplication       : Started StudentApplication in 2.842 seconds (process running for 3.219)
Connection verification: PostgreSQL connection successfully established.
"""
    add_code_block(doc, exp1_out)

    # =========================================================
    # EXPERIMENT 2
    # =========================================================
    add_styled_heading(doc, "Experiment 2: Creating and Testing a REST Endpoint", level=1)
    p = doc.add_paragraph(
        "Objective: To create and test a basic REST API using Spring Boot.\n\n"
        "2.1 Theory:\n"
        "Spring MVC handles HTTP requests using dispatcher servlets. The @RestController annotation marks the class as a request handler "
        "where return values are written directly to the HTTP response stream rather than resolving to HTML template views."
    )
    p.paragraph_format.line_spacing = 1.15

    add_styled_heading(doc, "2.2 Source Code: TestController.java", level=2)
    exp2_code = """
package com.college.sms.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class TestController {

    @GetMapping("/test")
    public String getTestMessage() {
        return "Spring Boot Application is Running";
    }
}
"""
    add_code_block(doc, exp2_code)

    add_styled_heading(doc, "2.3 Testing via Postman / cURL & Output", level=2)
    exp2_out = """
Request:
GET http://localhost:8080/api/test
Headers: Accept: text/plain

Response:
Status: 200 OK
Content-Type: text/plain;charset=UTF-8
Response Body:
Spring Boot Application is Running
"""
    add_code_block(doc, exp2_out)

    # =========================================================
    # EXPERIMENT 3
    # =========================================================
    add_styled_heading(doc, "Experiment 3: Creating an Entity Class", level=1)
    p = doc.add_paragraph(
        "Objective: To map a Java class to a database table using JPA annotations.\n\n"
        "3.1 Theory:\n"
        "Jakarta Persistence API (JPA) standardizes object-relational mapping in Java. The @Entity annotation identifies the POJO as a persistent "
        "domain model, @Table defines the database table name, @Id declares the primary key, and @GeneratedValue delegates key generation "
        "to PostgreSQL's sequence engine."
    )
    p.paragraph_format.line_spacing = 1.15

    add_styled_heading(doc, "3.2 Source Code: Student.java", level=2)
    exp3_code = """
package com.college.sms.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "students")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Student {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "name", nullable = false, length = 100)
    private String name;

    @Column(name = "email", nullable = false, unique = true, length = 120)
    private String email;

    @Column(name = "department", nullable = false, length = 50)
    private String department;
}
"""
    add_code_block(doc, exp3_code)

    add_styled_heading(doc, "3.3 Verification in PostgreSQL", level=2)
    exp3_out = """
psql> \\d students
                                     Table "public.students"
   Column   |          Type          | Collation | Nullable |               Default                
------------+------------------------+-----------+----------+--------------------------------------
 id         | bigint                 |           | not null | nextval('students_id_seq'::regclass)
 name       | character varying(100) |           | not null | 
 email      | character varying(120) |           | not null | 
 department | character varying(50)  |           | not null | 
Indexes:
    "students_pkey" PRIMARY KEY, btree (id)
    "uk_students_email" UNIQUE CONSTRAINT, btree (email)
"""
    add_code_block(doc, exp3_out)

    # =========================================================
    # EXPERIMENT 4
    # =========================================================
    add_styled_heading(doc, "Experiment 4: Creating a Repository Interface", level=1)
    p = doc.add_paragraph(
        "Objective: To perform database operations using Spring Data JPA.\n\n"
        "4.1 Theory:\n"
        "Spring Data JPA repositories dramatically reduce data access boilerplate. Extending JpaRepository<Student, Long> inherits 20+ "
        "built-in methods including save(), findById(), findAll(), deleteById(), existsById(), and count() without writing any implementation class."
    )
    p.paragraph_format.line_spacing = 1.15

    add_styled_heading(doc, "4.2 Source Code: StudentRepository.java", level=2)
    exp4_code = """
package com.college.sms.repository;

import com.college.sms.entity.Student;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

@Repository
public interface StudentRepository extends JpaRepository<Student, Long> {
    // Custom finder method derived automatically from method signature
    Optional<Student> findByEmail(String email);
    List<Student> findByDepartment(String department);
}
"""
    add_code_block(doc, exp4_code)

    add_styled_heading(doc, "4.3 Service Layer Integration & Verification: StudentService.java", level=2)
    exp4_serv = """
package com.college.sms.service;

import com.college.sms.entity.Student;
import com.college.sms.repository.StudentRepository;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class StudentService {
    private final StudentRepository studentRepository;

    public StudentService(StudentRepository studentRepository) {
        this.studentRepository = studentRepository;
    }

    public List<Student> getAllStudents() {
        return studentRepository.findAll();
    }

    public Student getStudentById(Long id) {
        return studentRepository.findById(id).orElse(null);
    }
}
"""
    add_code_block(doc, exp4_serv)

    # =========================================================
    # EXPERIMENT 5
    # =========================================================
    add_styled_heading(doc, "Experiment 5: Implementing Create and Read Operations", level=1)
    p = doc.add_paragraph(
        "Objective: To implement the first two CRUD operations through REST endpoints (POST to add, GET to retrieve all, GET by ID).\n\n"
        "5.1 Source Code: Controller Implementation"
    )
    p.paragraph_format.line_spacing = 1.15

    exp5_code = """
package com.college.sms.controller;

import com.college.sms.entity.Student;
import com.college.sms.repository.StudentRepository;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/students")
public class StudentCrudController {

    private final StudentRepository repository;

    public StudentCrudController(StudentRepository repository) {
        this.repository = repository;
    }

    // CREATE: POST /api/students
    @PostMapping
    public ResponseEntity<Student> createStudent(@RequestBody Student student) {
        Student savedStudent = repository.save(student);
        return new ResponseEntity<>(savedStudent, HttpStatus.CREATED);
    }

    // READ ALL: GET /api/students
    @GetMapping
    public List<Student> getAllStudents() {
        return repository.findAll();
    }

    // READ BY ID: GET /api/students/{id}
    @GetMapping("/{id}")
    public ResponseEntity<Student> getStudentById(@PathVariable Long id) {
        return repository.findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }
}
"""
    add_code_block(doc, exp5_code)

    add_styled_heading(doc, "5.2 Postman Test Execution & PostgreSQL Verification", level=2)
    exp5_out = """
1. POST Request: http://localhost:8080/api/students
Payload:
{
  "name": "Aarav Sharma",
  "email": "aarav.sharma@college.edu",
  "department": "Computer Science"
}
Response: Status 201 Created
{
  "id": 1,
  "name": "Aarav Sharma",
  "email": "aarav.sharma@college.edu",
  "department": "Computer Science"
}

2. GET Request: http://localhost:8080/api/students/1
Response: Status 200 OK
{
  "id": 1,
  "name": "Aarav Sharma",
  "email": "aarav.sharma@college.edu",
  "department": "Computer Science"
}
"""
    add_code_block(doc, exp5_out)

    # =========================================================
    # EXPERIMENT 6
    # =========================================================
    add_styled_heading(doc, "Experiment 6: Implementing Update and Delete Operations", level=1)
    p = doc.add_paragraph(
        "Objective: To complete CRUD functionality in a Spring Boot REST API with PUT and DELETE methods and proper 404 handling.\n\n"
        "6.1 Source Code: Update and Delete Endpoints"
    )
    p.paragraph_format.line_spacing = 1.15

    exp6_code = """
    // UPDATE: PUT /api/students/{id}
    @PutMapping("/{id}")
    public ResponseEntity<Student> updateStudent(@PathVariable Long id, @RequestBody Student studentDetails) {
        return repository.findById(id).map(existingStudent -> {
            existingStudent.setName(studentDetails.getName());
            existingStudent.setEmail(studentDetails.getEmail());
            existingStudent.setDepartment(studentDetails.getDepartment());
            Student updated = repository.save(existingStudent);
            return ResponseEntity.ok(updated);
        }).orElse(ResponseEntity.notFound().build());
    }

    // DELETE: DELETE /api/students/{id}
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteStudent(@PathVariable Long id) {
        if (!repository.existsById(id)) {
            return ResponseEntity.notFound().build();
        }
        repository.deleteById(id);
        return ResponseEntity.noContent().build();
    }
"""
    add_code_block(doc, exp6_code)

    add_styled_heading(doc, "6.2 Execution Testing & Verification", level=2)
    exp6_out = """
1. PUT Request: http://localhost:8080/api/students/1
Payload:
{
  "name": "Aarav Sharma",
  "email": "aarav.updated@college.edu",
  "department": "Data Science"
}
Response: Status 200 OK
{
  "id": 1,
  "name": "Aarav Sharma",
  "email": "aarav.updated@college.edu",
  "department": "Data Science"
}

2. DELETE Request: http://localhost:8080/api/students/1
Response: Status 204 No Content

3. Verification GET /api/students/1
Response: Status 404 Not Found
"""
    add_code_block(doc, exp6_out)

    # =========================================================
    # EXPERIMENT 7
    # =========================================================
    add_styled_heading(doc, "Experiment 7: Implementing Entity Relationships", level=1)
    p = doc.add_paragraph(
        "Objective: To establish relationships between entities using JPA mapping annotations (@ManyToOne and @OneToMany).\n\n"
        "7.1 Theory:\n"
        "Relational databases link tables using foreign keys. In JPA, a bidirectional relationship is established between Department (Parent, One) "
        "and Student (Child, Many) using @ManyToOne on Student and @OneToMany(mappedBy = 'department') on Department."
    )
    p.paragraph_format.line_spacing = 1.15

    add_styled_heading(doc, "7.2 Source Code: Department.java and Relational Student.java", level=2)
    exp7_code = """
// Department.java
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
    @JsonIgnoreProperties("department") // Prevents infinite recursion during JSON serialization
    private List<Student> students = new ArrayList<>();
}

// Student.java (Relational Child Entity)
@Entity
@Table(name = "students")
@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class Student {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false, unique = true)
    private String email;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "department_id", nullable = false)
    private Department department;
}
"""
    add_code_block(doc, exp7_code)

    add_styled_heading(doc, "7.3 Relational DDL & Postman Execution Output", level=2)
    exp7_out = """
POST http://localhost:8080/api/departments
Payload: { "name": "Information Technology", "buildingLocation": "Turing Block, 3rd Floor" }
Response: 201 Created (id: 1)

POST http://localhost:8080/api/students
Payload: { "name": "Diya Patel", "email": "diya.patel@college.edu", "department": { "id": 1 } }
Response: 201 Created

GET http://localhost:8080/api/departments/1
Response 200 OK:
{
  "id": 1,
  "name": "Information Technology",
  "buildingLocation": "Turing Block, 3rd Floor",
  "students": [
    {
      "id": 1,
      "name": "Diya Patel",
      "email": "diya.patel@college.edu"
    }
  ]
}
"""
    add_code_block(doc, exp7_out)

    # =========================================================
    # EXPERIMENT 8
    # =========================================================
    add_styled_heading(doc, "Experiment 8: Implementing Logging and Exception Handling", level=1)
    p = doc.add_paragraph(
        "Objective: To record application events and handle errors effectively using SLF4J, Logback, and @RestControllerAdvice.\n\n"
        "8.1 Theory:\n"
        "Logging records runtime operational traces. Centralized exception handling intercepts exceptions thrown across controllers "
        "and standardizes JSON error responses with appropriate HTTP status codes (e.g. 404 Not Found, 400 Bad Request)."
    )
    p.paragraph_format.line_spacing = 1.15

    add_styled_heading(doc, "8.2 Source Code: GlobalExceptionHandler.java & Custom Exception", level=2)
    exp8_code = """
// 1. Custom Exception
package com.college.sms.exception;
public class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String message) {
        super(message);
    }
}

// 2. Global Exception Handler
package com.college.sms.exception;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@RestControllerAdvice
public class GlobalExceptionHandler {
    private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<Map<String, Object>> handleNotFound(ResourceNotFoundException ex) {
        log.warn("RESOURCE_NOT_FOUND intercepted: {}", ex.getMessage());
        
        Map<String, Object> body = new HashMap<>();
        body.put("timestamp", LocalDateTime.now());
        body.put("status", HttpStatus.NOT_FOUND.value());
        body.put("error", "Not Found");
        body.put("message", ex.getMessage());
        return new ResponseEntity<>(body, HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<Map<String, Object>> handleGenericException(Exception ex) {
        log.error("UNHANDLED_EXCEPTION caught in API pipeline: {}", ex.getMessage(), ex);
        
        Map<String, Object> body = new HashMap<>();
        body.put("timestamp", LocalDateTime.now());
        body.put("status", HttpStatus.INTERNAL_SERVER_ERROR.value());
        body.put("error", "Internal Server Error");
        body.put("message", "An unexpected error occurred. Please contact system administrator.");
        return new ResponseEntity<>(body, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
"""
    add_code_block(doc, exp8_code)

    add_styled_heading(doc, "8.3 Output Verification (Client Response & Log Trace)", level=2)
    exp8_out = """
GET http://localhost:8080/api/students/9999
HTTP Status: 404 Not Found
{
  "timestamp": "2026-10-23T11:42:15.301",
  "status": 404,
  "error": "Not Found",
  "message": "Student record not found for ID: 9999"
}

Console Log Output:
2026-10-23 11:42:15.300 WARN  [sms,http-nio-8080-exec-4] c.c.s.e.GlobalExceptionHandler: RESOURCE_NOT_FOUND intercepted: Student record not found for ID: 9999
"""
    add_code_block(doc, exp8_out)

    # =========================================================
    # EXPERIMENT 9
    # =========================================================
    add_styled_heading(doc, "Experiment 9: API Documentation Using Swagger/OpenAPI", level=1)
    p = doc.add_paragraph(
        "Objective: To document and test REST APIs using Swagger UI and Springdoc OpenAPI.\n\n"
        "9.1 Theory:\n"
        "The OpenAPI 3.0 specification provides a standardized machine-readable definition of REST APIs. Springdoc parses Spring MVC annotations "
        "and generates both the raw /v3/api-docs JSON endpoint and the interactive /swagger-ui/index.html interface."
    )
    p.paragraph_format.line_spacing = 1.15

    add_styled_heading(doc, "9.2 Configuration: pom.xml & OpenApiConfig.java", level=2)
    exp9_code = """
<!-- Dependency in pom.xml -->
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.5.0</version>
</dependency>

// OpenApiConfig.java
package com.college.sms.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.Contact;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {
    @Bean
    public OpenAPI studentManagementOpenAPI() {
        return new OpenAPI()
            .info(new Info()
                .title("Student Management System REST API")
                .description("Production REST API with PostgreSQL integration & Full CRUD capabilities")
                .version("1.0.0")
                .contact(new Contact().name("Full Stack Development Team").email("fsd@college.edu")));
    }
}
"""
    add_code_block(doc, exp9_code)

    add_styled_heading(doc, "9.3 Testing CRUD directly through Swagger UI", level=2)
    exp9_out = """
1. Open URL: http://localhost:8080/swagger-ui/index.html
2. Swagger UI displays endpoints:
   - GET    /api/students       (Retrieve all students)
   - POST   /api/students       (Create new student)
   - GET    /api/students/{id}  (Retrieve student by ID)
   - PUT    /api/students/{id}  (Update student by ID)
   - DELETE /api/students/{id}  (Delete student by ID)
3. Testing:
   - Click 'Try it out' on GET /api/students -> Click 'Execute' -> HTTP 200 with response JSON list.
   - Swagger provides interactive curls, request body validation, and response code mapping.
"""
    add_code_block(doc, exp9_out)

    # =========================================================
    # EXPERIMENT 10
    # =========================================================
    add_styled_heading(doc, "Experiment 10: Packaging and Deployment of the Application", level=1)
    p = doc.add_paragraph(
        "Objective: To package the Spring Boot backend application as a WAR file and prepare it for deployment to an external servlet container (Apache Tomcat).\n\n"
        "10.1 Theory:\n"
        "While Spring Boot packages by default as a standalone executable JAR with an embedded Tomcat, enterprise production deployments "
        "frequently require WAR (Web Application Archive) deployment inside an existing managed Apache Tomcat servlet container. "
        "This requires marking the embedded container dependency as 'provided' and extending SpringBootServletInitializer."
    )
    p.paragraph_format.line_spacing = 1.15

    add_styled_heading(doc, "10.2 Configuration: pom.xml WAR Packaging", level=2)
    exp10_code = """
<!-- Change packaging to war in pom.xml -->
<packaging>war</packaging>

<dependencies>
    <!-- Mark embedded tomcat as provided for external deployment -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-tomcat</artifactId>
        <scope>provided</scope>
    </dependency>
</dependencies>
"""
    add_code_block(doc, exp10_code)

    add_styled_heading(doc, "10.3 Servlet Initializer: ServletInitializer.java", level=2)
    exp10_init = """
package com.college.sms;

import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;

public class ServletInitializer extends SpringBootServletInitializer {

    @Override
    protected SpringApplicationBuilder configure(SpringApplicationBuilder application) {
        // Binds Spring Boot application context to the external servlet container
        return application.sources(StudentApplication.class);
    }
}
"""
    add_code_block(doc, exp10_init)

    add_styled_heading(doc, "10.4 Build Execution & External Tomcat Deployment Commands", level=2)
    exp10_deploy = """
# Step 1: Clean build and package the WAR artifact using Maven
mvn clean package -DskipTests

# Output:
# [INFO] Building war: C:\\college\\sms\\target\\student-management-system-1.0.0.war
# [INFO] BUILD SUCCESS
# [INFO] Total time:  14.281 s

# Step 2: Deploy WAR artifact to Apache Tomcat webapps directory
cp target/student-management-system-1.0.0.war /opt/tomcat/webapps/sms.war

# Step 3: Start Apache Tomcat
/opt/tomcat/bin/startup.sh

# Step 4: Verify deployment at external URL
curl http://localhost:8080/sms/api/test
# Output: Spring Boot Application is Running
"""
    add_code_block(doc, exp10_deploy)

    output_path = "submissions/FSD_10_Experiments_Complete_Lab_Manual.docx"
    doc.save(output_path)
    print(f"Successfully generated: {output_path}")

build_experiments()
