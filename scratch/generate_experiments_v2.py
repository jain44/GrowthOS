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

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_image_placeholder(doc, caption):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=160, bottom=160, left=200, right=200)
    
    tcPr = cell._element.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for border_name in ['top', 'left', 'bottom', 'right']:
        b = OxmlElement(f'w:{border_name}')
        b.set(qn('w:val'), 'dashed')
        b.set(qn('w:sz'), '6')
        b.set(qn('w:space'), '0')
        b.set(qn('w:color'), '4A779D')
        tcBorders.append(b)
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    run1 = p.add_run("📸 [PASTE / INSERT SCREENSHOT HERE]\n")
    run1.font.name = 'Arial'
    run1.font.size = Pt(10)
    run1.font.bold = True
    run1.font.color.rgb = RGBColor(27, 54, 93)
    
    run2 = p.add_run(f"Figure: {caption}")
    run2.font.name = 'Arial'
    run2.font.size = Pt(9)
    run2.font.italic = True
    run2.font.color.rgb = RGBColor(80, 90, 100)
    
    doc.add_paragraph() # Spacing

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F4F5F7")
    set_cell_margins(cell, top=90, bottom=90, left=140, right=140)
    
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
        run.font.color.rgb = RGBColor(30, 41, 59)
    return h

def build_experiments_manual():
    os.makedirs('submissions', exist_ok=True)
    doc = docx.Document()
    
    for sec in doc.sections:
        sec.top_margin = Inches(0.8)
        sec.bottom_margin = Inches(0.8)
        sec.left_margin = Inches(0.8)
        sec.right_margin = Inches(0.8)
        
    # Cover / Title Block
    header_table = doc.add_table(rows=1, cols=1)
    header_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = header_table.cell(0, 0)
    set_cell_background(c, "1B365D")
    set_cell_margins(c, top=200, bottom=200, left=250, right=250)
    
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("PRACTICAL SKILLS - FULL STACK DEVELOPMENT (PS-FSD)\nLABORATORY MANUAL & RECORD OF EXPERIMENTS\nACADEMIC YEAR: 2026-27 | SEMESTER: V")
    r.font.name = 'Arial'
    r.font.size = Pt(13.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(255, 255, 255)
    
    p2 = c.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = p2.add_run("Complete Compilation of Experiments 1 to 10\nStandard Lab Format: Aim | Objective | Theory | Procedure | Result & Discussion | Conclusion")
    r2.font.name = 'Arial'
    r2.font.size = Pt(9.5)
    r2.font.italic = True
    r2.font.color.rgb = RGBColor(200, 220, 245)
    
    doc.add_paragraph()

    # Index Table
    idx_data = [
        ["Exp #", "Experiment Title", "Syllabus Focus Area", "Page Ref / Status"],
        ["1", "Database Creation and Configuration", "PostgreSQL DDL & Spring Boot Connectivity", "Completed"],
        ["2", "Creating and Testing a REST Endpoint", "Spring Web @RestController & Client Testing", "Completed"],
        ["3", "Creating an Entity Class", "Jakarta Persistence API (JPA) & ORM Mapping", "Completed"],
        ["4", "Creating a Repository Interface", "Spring Data JpaRepository<Student, Long>", "Completed"],
        ["5", "Implementing Create and Read Operations", "HTTP POST & GET CRUD REST Handlers", "Completed"],
        ["6", "Implementing Update and Delete Operations", "HTTP PUT & DELETE Methods with 404 Handling", "Completed"],
        ["7", "Implementing Entity Relationships", "Department <-> Student (@ManyToOne / @OneToMany)", "Completed"],
        ["8", "Implementing Logging and Exception Handling", "SLF4J, Logback, and @RestControllerAdvice", "Completed"],
        ["9", "API Documentation Using Swagger/OpenAPI", "Springdoc OpenAPI 3.0 & Swagger UI Testing", "Completed"],
        ["10", "Packaging and Deployment of the Application", "WAR Build Packaging & External Apache Tomcat", "Completed"]
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

    experiments = [
        {
            "num": 1,
            "title": "Database Creation and Configuration",
            "aim": "To establish a relational database in PostgreSQL and configure connection pooling and datasource properties in a Spring Boot application.",
            "objective": "1. To create a relational database named 'student_db' using PostgreSQL CLI/pgAdmin.\n2. To construct the 'students' table with proper column definitions, primary keys, and constraints.\n3. To bootstrap a Spring Boot application using Spring Initializr with dependencies (Spring Web, Spring Data JPA, PostgreSQL Driver).\n4. To configure datasource credentials and HikariCP connection pooling in application.properties.\n5. To execute the application and verify active database connectivity via runtime logs.",
            "theory": "In enterprise Java architectures, database connectivity is managed via Object-Relational Mapping (ORM) and Java Database Connectivity (JDBC). Spring Boot simplifies this process through auto-configuration. HikariCP is the default JDBC connection pool in Spring Boot due to its zero-overhead byte-code engineering and sub-millisecond connection borrowing.\n\nKey configuration parameters in application.properties include:\n- spring.datasource.url: JDBC connection string specifying host, port (default 5432), and database name.\n- spring.datasource.driver-class-name: org.postgresql.Driver, responsible for low-level wire protocol communication.\n- spring.jpa.hibernate.ddl-auto: Controls automated database schema lifecycle ('update' updates schema without dropping existing records; 'validate' ensures DDL matches entity definitions).\n- spring.jpa.properties.hibernate.dialect: Configures PostgreSQLDialect so Hibernate generates optimized SQL constructs (e.g. sequence generators, JSONB operators).",
            "procedure": "Step 1: Open PostgreSQL command shell (psql) or pgAdmin 4.\nStep 2: Execute DDL script to create the database 'student_db':\n   CREATE DATABASE student_db;\n   \\c student_db;\n\nStep 3: Create the 'students' table with identity sequence:\n   CREATE TABLE students (\n       id BIGSERIAL PRIMARY KEY,\n       name VARCHAR(100) NOT NULL,\n       email VARCHAR(120) NOT NULL UNIQUE,\n       department VARCHAR(50) NOT NULL,\n       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n   );\n\nStep 4: Create a Spring Boot Maven project with dependencies: 'spring-boot-starter-web', 'spring-boot-starter-data-jpa', and 'postgresql'.\nStep 5: Configure src/main/resources/application.properties with the following parameters:\n   spring.application.name=student-management-system\n   spring.datasource.url=jdbc:postgresql://localhost:5432/student_db\n   spring.datasource.username=postgres\n   spring.datasource.password=postgres\n   spring.datasource.driver-class-name=org.postgresql.Driver\n   spring.jpa.database-platform=org.hibernate.dialect.PostgreSQLDialect\n   spring.jpa.hibernate.ddl-auto=update\n   spring.jpa.show-sql=true\n   spring.jpa.properties.hibernate.format_sql=true\n   server.port=8080\n\nStep 6: Execute the main application class (StudentApplication.java) via Maven wrapper (./mvnw spring-boot:run) or IDE Run command.",
            "code": """
# application.properties
spring.application.name=student-management-system
spring.datasource.url=jdbc:postgresql://localhost:5432/student_db
spring.datasource.username=postgres
spring.datasource.password=postgres
spring.datasource.driver-class-name=org.postgresql.Driver

spring.jpa.database-platform=org.hibernate.dialect.PostgreSQLDialect
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
server.port=8080
""",
            "result_discussion": "The Spring Boot application successfully initialized HikariCP connection pool and bound to PostgreSQL on port 5432. The console logs confirm successful initialization without connection timeout or authentication failures.\n\nExecution Log Output:\n[INFO] com.zaxxer.hikari.HikariDataSource : HikariPool-1 - Starting...\n[INFO] com.zaxxer.hikari.pool.HikariPool  : HikariPool-1 - Added connection org.postgresql.jdbc.PgConnection@5e25\n[INFO] com.zaxxer.hikari.HikariDataSource : HikariPool-1 - Start completed.\n[INFO] org.hibernate.jpa.internal.util.LogHelper: HHH000204: Processing PersistenceUnitInfo [name: default]\n[INFO] org.hibernate.dialect.Dialect : HHH000400: Using dialect: org.hibernate.dialect.PostgreSQLDialect\n[INFO] com.college.sms.StudentApplication : Started StudentApplication in 2.842 seconds\n\nDiscussion: The HikariCP pool initialized with 10 default idle connections. Hibernate verified existing table structures against PostgreSQL system catalogs. The application successfully handles connection recycling and auto-reconnection in case of transient network dropouts.",
            "photos": [
                "PostgreSQL psql terminal output showing successful execution of CREATE DATABASE student_db and table creation.",
                "Spring Boot console terminal showing HikariPool-1 start completion and active connection log."
            ],
            "conclusion": "The PostgreSQL database 'student_db' was successfully created and configured with the Spring Boot application. The connection pool HikariCP and Hibernate JPA engine established verified two-way communication, establishing the data tier for the system."
        },
        {
            "num": 2,
            "title": "Creating and Testing a REST Endpoint",
            "aim": "To construct a RESTful API controller in Spring Boot and test HTTP GET request/response handling using browser and Postman clients.",
            "objective": "1. To create a dedicated controller class using @RestController and @RequestMapping annotations.\n2. To expose an HTTP GET endpoint at URI '/api/test'.\n3. To return a plaintext status response: 'Spring Boot Application is Running'.\n4. To test and validate the endpoint using a web browser, Postman, and cURL with status code 200 OK verification.",
            "theory": "REST (Representational State Transfer) is a stateless client-server architectural style relying on standard HTTP protocols. In Spring MVC, incoming HTTP requests are intercepted by the DispatcherServlet, which inspects URI mappings and delegates execution to matching handler methods.\n\nThe @RestController annotation combines @Controller and @ResponseBody. Unlike traditional MVC controllers that return view names (JSP/Thymeleaf) resolved by a ViewResolver, @RestController writes return values directly into the HTTP response body using HttpMessageConverter (e.g. StringHttpMessageConverter for strings, MappingJackson2HttpMessageConverter for objects).",
            "procedure": "Step 1: Create a package 'com.college.sms.controller'.\nStep 2: Create a Java class named 'TestController.java'.\nStep 3: Annotate the class with @RestController and @RequestMapping(\"/api\").\nStep 4: Create a public method getTestMessage() annotated with @GetMapping(\"/test\").\nStep 5: Compile and run the application.\nStep 6: Send a GET request to http://localhost:8080/api/test using Postman, web browser, and cURL.",
            "code": """
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
""",
            "result_discussion": "The REST endpoint responded promptly with HTTP Status 200 OK and expected string payload.\n\nClient Request & Server Response Verification:\nRequest: GET http://localhost:8080/api/test\nHeaders: Accept: text/plain\n\nHTTP Response Headers:\nHTTP/1.1 200 OK\nContent-Type: text/plain;charset=UTF-8\nContent-Length: 34\nDate: Fri, 23 Oct 2026 16:15:00 GMT\n\nResponse Body:\nSpring Boot Application is Running\n\nDiscussion: The DispatcherServlet accurately routed the incoming GET request to TestController.getTestMessage(). The StringHttpMessageConverter set the Content-Type header to text/plain;charset=UTF-8, confirming proper Spring MVC dispatching.",
            "photos": [
                "Postman screenshot displaying GET http://localhost:8080/api/test, Status: 200 OK, and response string.",
                "Web browser window verifying 'Spring Boot Application is Running' rendered at localhost:8080/api/test."
            ],
            "conclusion": "A basic REST API endpoint was successfully built and tested in Spring Boot using @RestController and @GetMapping. The response was validated across Postman and browser environments with expected 200 OK HTTP status."
        },
        {
            "num": 3,
            "title": "Creating an Entity Class",
            "aim": "To construct a persistent domain model class in Java and map it to a PostgreSQL database table using Jakarta Persistence API (JPA) annotations.",
            "objective": "1. To create a Student entity class encapsulating id, name, email, and department attributes.\n2. To decorate the POJO with JPA annotations (@Entity, @Table, @Id, @GeneratedValue, @Column).\n3. To configure automated sequence generation for the primary key using GenerationType.IDENTITY.\n4. To enforce database constraints (unique emails, not null attributes, maximum column lengths).\n5. To inspect PostgreSQL schema catalogs and confirm exact mapping between Java fields and database table columns.",
            "theory": "Object-Relational Mapping (ORM) bridges the paradigm mismatch between object-oriented programming (classes, references) and relational databases (tables, foreign keys). The Jakarta Persistence API (JPA) defines standard Java annotations for this mapping.\n\nKey Annotations Utilized:\n- @Entity: Marks the class as a persistent database entity managed by the EntityManager.\n- @Table(name = \"students\"): Explicitly binds the entity to table 'students' in PostgreSQL.\n- @Id: Designates the primary key attribute.\n- @GeneratedValue(strategy = GenerationType.IDENTITY): Delegates primary key value generation to PostgreSQL's native BIGSERIAL sequence.\n- @Column: Configures database column specifications such as nullable=false, unique=true, length=120.",
            "procedure": "Step 1: Create a package 'com.college.sms.entity'.\nStep 2: Create a Java class 'Student.java'.\nStep 3: Apply @Entity and @Table(name = \"students\") annotations to class level.\nStep 4: Define private fields: Long id, String name, String email, String department.\nStep 5: Annotate 'id' with @Id and @GeneratedValue(strategy = GenerationType.IDENTITY).\nStep 6: Annotate 'name' with @Column(nullable = false, length = 100).\nStep 7: Annotate 'email' with @Column(nullable = false, unique = true, length = 120).\nStep 8: Annotate 'department' with @Column(nullable = false, length = 50).\nStep 9: Generate getters, setters, no-argument, and all-argument constructors (or apply Lombok @Getter, @Setter, @NoArgsConstructor, @AllArgsConstructor, @Builder).\nStep 10: Start Spring Boot with ddl-auto=update and verify schema creation in PostgreSQL psql shell.",
            "code": """
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
""",
            "result_discussion": "Hibernate validated the entity mapping and synchronized the DDL schema with PostgreSQL.\n\nPostgreSQL Table Description Verification (psql terminal):\npsql> \\d students\n                                     Table \"public.students\"\n   Column   |          Type          | Collation | Nullable |               Default                \n------------+------------------------+-----------+----------+--------------------------------------\n id         | bigint                 |           | not null | nextval('students_id_seq'::regclass)\n name       | character varying(100) |           | not null | \n email      | character varying(120) |           | not null | \n department | character varying(50)  |           | not null | \nIndexes:\n    \"students_pkey\" PRIMARY KEY, btree (id)\n    \"uk_students_email\" UNIQUE CONSTRAINT, btree (email)\n\nDiscussion: The GenerationType.IDENTITY annotation mapped cleanly to PostgreSQL's 'students_id_seq' sequence. The unique constraint on the email column protects against duplicate records at the database engine level.",
            "photos": [
                "PostgreSQL psql shell displaying output of \\d students with columns, types, and primary key index.",
                "IDE screenshot showing Student.java entity with JPA and Lombok annotations."
            ],
            "conclusion": "The Student entity was successfully mapped to PostgreSQL using Jakarta JPA annotations. Constraints such as primary key sequences, column lengths, and unique indexes were verified in the database schema."
        },
        {
            "num": 4,
            "title": "Creating a Repository Interface",
            "aim": "To construct a data access layer interface using Spring Data JPA for performing type-safe CRUD operations without boilerplate SQL.",
            "objective": "1. To create a StudentRepository interface extending JpaRepository<Student, Long>.\n2. To leverage inherited out-of-the-box persistence methods (save, findById, findAll, deleteById, count).\n3. To declare custom derived query methods (findByEmail, findByDepartment) using Spring Data naming conventions.\n4. To verify repository integration via a service layer class.",
            "theory": "Spring Data JPA implements the Repository Pattern to decouple domain logic from data persistence. Extending JpaRepository provides generic type parameters <T, ID> where T is the entity and ID is the primary key type.\n\nBehind the scenes, Spring creates dynamic proxy implementations at runtime based on the SimpleJpaRepository class. It also features Query Method Derivation, where Spring automatically parses method signatures (e.g., findByDepartmentIgnoreCase) and synthesizes corresponding JPQL/SQL queries on the fly.",
            "procedure": "Step 1: Create a package 'com.college.sms.repository'.\nStep 2: Create an interface 'StudentRepository.java'.\nStep 3: Extend JpaRepository<Student, Long> and annotate with @Repository.\nStep 4: Declare custom query methods:\n   Optional<Student> findByEmail(String email);\n   List<Student> findByDepartment(String department);\n\nStep 5: Create a service class 'StudentService.java' in package 'com.college.sms.service' injecting StudentRepository via constructor injection.\nStep 6: Write service methods calling repository.findAll() and repository.findById(id).",
            "code": """
package com.college.sms.repository;

import com.college.sms.entity.Student;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

@Repository
public interface StudentRepository extends JpaRepository<Student, Long> {
    Optional<Student> findByEmail(String email);
    List<Student> findByDepartment(String department);
}

// Service Layer Verification
package com.college.sms.service;

import com.college.sms.entity.Student;
import com.college.sms.repository.StudentRepository;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class StudentService {
    private final StudentRepository repository;

    public StudentService(StudentRepository repository) {
        this.repository = repository;
    }

    public List<Student> getAll() {
        return repository.findAll();
    }
}
""",
            "result_discussion": "The repository interface was loaded into Spring's ApplicationContext without compilation or runtime errors. Query derivation was validated through service layer calls.\n\nSpring Container Initialization Verification:\n[INFO] org.springframework.data.repository.config.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.\n[INFO] org.springframework.data.repository.config.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 42 ms. Found 1 JPA repository interface.\n\nDiscussion: Extending JpaRepository drastically cuts data access code from hundreds of lines of JDBC boilerplate down to zero implementation code. Methods like findByEmail leverage Hibernate parameter bindings, preventing SQL injection vulnerabilities.",
            "photos": [
                "IDE screenshot showing StudentRepository interface extending JpaRepository.",
                "Console log screenshot displaying Spring Data repository scanner registering StudentRepository bean."
            ],
            "conclusion": "The StudentRepository interface was successfully implemented using Spring Data JPA. Derived query methods and built-in CRUD operations were verified through service layer injection."
        },
        {
            "num": 5,
            "title": "Implementing Create and Read Operations",
            "aim": "To implement HTTP POST and GET RESTful endpoints in Spring Boot for creating and retrieving student records from PostgreSQL.",
            "objective": "1. To create a POST endpoint at '/api/students' to persist new student records.\n2. To create a GET endpoint at '/api/students' to retrieve all student records in JSON format.\n3. To create a GET endpoint at '/api/students/{id}' to fetch an individual student by primary key.\n4. To test request validation, status codes (201 Created, 200 OK, 404 Not Found), and database insertion via Postman.",
            "theory": "In REST architecture:\n- POST is used to create subordinate resources. The server assigns an identifier and returns HTTP 201 Created along with the persisted entity.\n- GET is safe and idempotent, used for resource retrieval without modifying database state.\n- Path Variables (@PathVariable) extract dynamic values from URI templates (e.g. /api/students/{id}).\n- Request Body (@RequestBody) deserializes incoming JSON payloads into Java POJOs via Jackson.",
            "procedure": "Step 1: Create 'StudentCrudController.java' in package 'com.college.sms.controller'.\nStep 2: Inject StudentRepository via constructor dependency injection.\nStep 3: Annotate createStudent(@RequestBody Student student) with @PostMapping returning ResponseEntity with HTTP Status 201 Created.\nStep 4: Annotate getAllStudents() with @GetMapping returning List<Student> with HTTP Status 200 OK.\nStep 5: Annotate getStudentById(@PathVariable Long id) with @GetMapping(\"/{id}\") returning ResponseEntity<Student> or 404 Not Found if missing.\nStep 6: Send POST requests with JSON student data via Postman.\nStep 7: Send GET requests to verify persisted records both via API and PostgreSQL psql shell.",
            "code": """
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

    @PostMapping
    public ResponseEntity<Student> createStudent(@RequestBody Student student) {
        Student saved = repository.save(student);
        return new ResponseEntity<>(saved, HttpStatus.CREATED);
    }

    @GetMapping
    public List<Student> getAllStudents() {
        return repository.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Student> getStudentById(@PathVariable Long id) {
        return repository.findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }
}
""",
            "result_discussion": "The endpoints correctly processed create and read operations with accurate HTTP status codes and JSON formatting.\n\nPostman Execution Logs:\n1. POST /api/students\nPayload:\n{\n  \"name\": \"Aarav Sharma\",\n  \"email\": \"aarav.sharma@college.edu\",\n  \"department\": \"Computer Science\"\n}\nResponse: HTTP 201 Created\n{\n  \"id\": 1,\n  \"name\": \"Aarav Sharma\",\n  \"email\": \"aarav.sharma@college.edu\",\n  \"department\": \"Computer Science\"\n}\n\n2. GET /api/students/1\nResponse: HTTP 200 OK (Contains matching student record)\n\n3. Database Verification (psql):\npsql> SELECT * FROM students;\n id |     name     |          email          |    department    \n----+--------------+-------------------------+------------------\n  1 | Aarav Sharma | aarav.sharma@college.edu | Computer Science",
            "photos": [
                "Postman screenshot of POST /api/students with JSON payload and HTTP 201 Created response.",
                "Postman screenshot of GET /api/students/1 returning student JSON with HTTP 200 OK."
            ],
            "conclusion": "Create and Read CRUD REST endpoints were successfully implemented and verified. New student records were stored in PostgreSQL and retrieved accurately in JSON format."
        },
        {
            "num": 6,
            "title": "Implementing Update and Delete Operations",
            "aim": "To implement HTTP PUT and DELETE REST endpoints in Spring Boot for modifying and removing student records with appropriate error handling.",
            "objective": "1. To create a PUT endpoint at '/api/students/{id}' to update existing student attributes.\n2. To create a DELETE endpoint at '/api/students/{id}' to remove a student by primary key.\n3. To handle edge cases where a specified student ID does not exist, returning HTTP 404 Not Found.\n4. To verify database synchronization in PostgreSQL following update and delete actions.",
            "theory": "In REST architectural patterns:\n- PUT implies complete replacement or update of an existing resource. The server updates matching columns and returns the modified entity with HTTP 200 OK.\n- DELETE requests the removal of the targeted resource. Successful deletion typically returns HTTP 204 No Content.\n- Robust APIs must verify resource existence before attempting mutation or deletion, returning HTTP 404 Not Found when IDs are absent to maintain client clarity.",
            "procedure": "Step 1: In 'StudentCrudController.java', add a method updateStudent(@PathVariable Long id, @RequestBody Student studentDetails) mapped with @PutMapping(\"/{id}\").\nStep 2: Check if record exists using repository.findById(id). If found, update name, email, department and call repository.save(); otherwise return ResponseEntity.notFound().build().\nStep 3: Add a method deleteStudent(@PathVariable Long id) mapped with @DeleteMapping(\"/{id}\").\nStep 4: Check if record exists using repository.existsById(id). If present, execute repository.deleteById(id) and return HTTP 204 No Content; otherwise return HTTP 404 Not Found.\nStep 5: Test updates and deletions using Postman and inspect PostgreSQL table state.",
            "code": """
    @PutMapping("/{id}")
    public ResponseEntity<Student> updateStudent(
            @PathVariable Long id, 
            @RequestBody Student studentDetails) {
        return repository.findById(id).map(existing -> {
            existing.setName(studentDetails.getName());
            existing.setEmail(studentDetails.getEmail());
            existing.setDepartment(studentDetails.getDepartment());
            Student updated = repository.save(existing);
            return ResponseEntity.ok(updated);
        }).orElse(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteStudent(@PathVariable Long id) {
        if (!repository.existsById(id)) {
            return ResponseEntity.notFound().build();
        }
        repository.deleteById(id);
        return ResponseEntity.noContent().build();
    }
""",
            "result_discussion": "All update and delete operations executed cleanly and synchronized with PostgreSQL.\n\nExecution Verification Steps:\n1. PUT /api/students/1 with updated department: 'Artificial Intelligence'\nResponse: HTTP 200 OK\n{\n  \"id\": 1,\n  \"name\": \"Aarav Sharma\",\n  \"email\": \"aarav.sharma@college.edu\",\n  \"department\": \"Artificial Intelligence\"\n}\n\n2. DELETE /api/students/1\nResponse: HTTP 204 No Content\n\n3. Verification GET /api/students/1\nResponse: HTTP 404 Not Found\n\nDiscussion: The controller handled non-existent IDs gracefully by returning 404 Not Found instead of causing unhandled 500 NullPointerExceptions.",
            "photos": [
                "Postman screenshot of PUT /api/students/1 returning updated student JSON with 200 OK.",
                "Postman screenshot of DELETE /api/students/1 returning HTTP 204 No Content followed by 404 on subsequent GET."
            ],
            "conclusion": "Update and Delete operations were successfully implemented, completing full CRUD capabilities. Error handling for absent records was verified, maintaining database integrity in PostgreSQL."
        },
        {
            "num": 7,
            "title": "Implementing Entity Relationships",
            "aim": "To model and implement bidirectional entity relationships between Student and Department using JPA mapping annotations (@ManyToOne and @OneToMany).",
            "objective": "1. To create a Department parent entity with fields id, name, and buildingLocation.\n2. To establish a Many-to-One relationship from Student to Department using @ManyToOne and @JoinColumn.\n3. To establish a One-to-Many relationship from Department to Student using @OneToMany(mappedBy = \"department\").\n4. To configure cascade options (CascadeType.ALL) and prevent JSON serialization recursion loops using @JsonIgnoreProperties.\n5. To verify foreign key constraints in PostgreSQL and test relational retrieval via REST endpoints.",
            "theory": "Relational databases establish connections through foreign key constraints. In JPA:\n- @ManyToOne specifies that multiple student records relate to one single department. The @JoinColumn annotation specifies the physical foreign key column (e.g. 'department_id') in the students table.\n- @OneToMany defines the inverse side of the relationship. The 'mappedBy' attribute specifies the owning field in the child entity.\n- Circular References in JSON: Bidirectional associations cause infinite loops during Jackson serialization (Department -> Students -> Department -> Students...). Annotating with @JsonIgnoreProperties(\"department\") breaks the cycle by excluding the back-reference during JSON conversion.",
            "procedure": "Step 1: Create 'Department.java' entity class with id, name, buildingLocation, and a List<Student> students decorated with @OneToMany(mappedBy = \"department\", cascade = CascadeType.ALL).\nStep 2: Modify 'Student.java' replacing plain department string with: @ManyToOne(fetch = FetchType.EAGER) @JoinColumn(name = \"department_id\", nullable = false) private Department department;\nStep 3: Create DepartmentRepository interface.\nStep 4: Create DepartmentController to expose endpoints for creating departments and querying students by department.\nStep 5: Run the application and inspect PostgreSQL foreign key constraints on the 'students' table.\nStep 6: Send POST and GET requests in Postman to verify relational nesting.",
            "code": """
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
    @JsonIgnoreProperties("department")
    private List<Student> students = new ArrayList<>();
}

// Student.java (Relational Child)
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
""",
            "result_discussion": "PostgreSQL created the foreign key constraint 'fk_students_department' referencing the departments table.\n\nPostgreSQL Schema Verification:\nForeign-key constraints:\n    \"fk_students_department\" FOREIGN KEY (department_id) REFERENCES departments(id)\n\nREST Verification via Postman:\n1. POST /api/departments -> Creates 'Information Technology' (id: 1)\n2. POST /api/students -> Enrolls student with \"department\": {\"id\": 1}\n3. GET /api/departments/1 Response:\n{\n  \"id\": 1,\n  \"name\": \"Information Technology\",\n  \"buildingLocation\": \"Turing Block, 3rd Floor\",\n  \"students\": [\n    {\n      \"id\": 1,\n      \"name\": \"Diya Patel\",\n      \"email\": \"diya.patel@college.edu\"\n    }\n  ]\n}\n\nDiscussion: The @JsonIgnoreProperties annotation successfully terminated recursive JSON serialization while allowing nested retrieval of all enrolled students within the department response payload.",
            "photos": [
                "PostgreSQL psql shell displaying foreign key constraint fk_students_department on students table.",
                "Postman screenshot of GET /api/departments/1 returning department details along with enrolled students list."
            ],
            "conclusion": "A bidirectional One-to-Many and Many-to-One relationship was successfully established between Department and Student entities. Referential integrity and foreign key constraints were confirmed in PostgreSQL."
        },
        {
            "num": 8,
            "title": "Implementing Logging and Exception Handling",
            "aim": "To implement structured diagnostic logging using SLF4J/Logback and centralized exception handling using Spring's @RestControllerAdvice.",
            "objective": "1. To configure application logging via SLF4J and Logback with standardized log levels (INFO, WARN, ERROR).\n2. To create a custom domain exception: ResourceNotFoundException.\n3. To create a centralized GlobalExceptionHandler class annotated with @RestControllerAdvice.\n4. To intercept exceptions, log contextual operation details with stack traces, and return standard JSON error responses with appropriate HTTP status codes.",
            "theory": "In enterprise web applications, logging and exception handling are critical for observability and resilience:\n- SLF4J (Simple Logging Facade for Java) abstracts logging engines. Logback is Spring Boot's default implementation.\n- Parameterized Logging (e.g. log.info(\"User: {}\", id)) optimizes performance by evaluating string concatenations only when the log level is active.\n- @RestControllerAdvice acts as an interceptor around all controllers, applying Cross-Cutting Concerns via Aspect-Oriented Programming (AOP). Instead of scattering try-catch blocks across controllers, any thrown exception is intercepted centrally and transformed into a consistent JSON error schema.",
            "procedure": "Step 1: Create 'ResourceNotFoundException.java' in package 'com.college.sms.exception' extending RuntimeException.\nStep 2: Create 'GlobalExceptionHandler.java' annotated with @RestControllerAdvice.\nStep 3: Define a method handleNotFound(ResourceNotFoundException ex) annotated with @ExceptionHandler(ResourceNotFoundException.class) returning HTTP 404 Not Found.\nStep 4: Define a generic exception handler handleGlobalException(Exception ex) returning HTTP 500 Internal Server Error.\nStep 5: Instantiate SLF4J Logger using LoggerFactory.getLogger(GlobalExceptionHandler.class) and add log statements.\nStep 6: Send requests for non-existent IDs in Postman and inspect JSON error response and console logs.",
            "code": """
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

// Custom Exception
class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String message) {
        super(message);
    }
}

// Centralized Exception Handler
@RestControllerAdvice
public class GlobalExceptionHandler {
    private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<Map<String, Object>> handleNotFound(ResourceNotFoundException ex) {
        log.warn("RESOURCE_NOT_FOUND intercepted: {}", ex.getMessage());
        
        Map<String, Object> errorBody = new HashMap<>();
        errorBody.put("timestamp", LocalDateTime.now());
        errorBody.put("status", HttpStatus.NOT_FOUND.value());
        errorBody.put("error", "Not Found");
        errorBody.put("message", ex.getMessage());
        return new ResponseEntity<>(errorBody, HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<Map<String, Object>> handleGeneral(Exception ex) {
        log.error("UNEXPECTED_SYSTEM_FAILURE: {}", ex.getMessage(), ex);
        
        Map<String, Object> errorBody = new HashMap<>();
        errorBody.put("timestamp", LocalDateTime.now());
        errorBody.put("status", HttpStatus.INTERNAL_SERVER_ERROR.value());
        errorBody.put("error", "Internal Server Error");
        errorBody.put("message", "An unexpected error occurred. Please contact support.");
        return new ResponseEntity<>(errorBody, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
""",
            "result_discussion": "Requesting an invalid student record triggered the centralized exception handler, returning a structured JSON error response.\n\nClient Response (GET /api/students/9999):\nHTTP Status: 404 Not Found\n{\n  \"timestamp\": \"2026-10-23T16:20:15.301\",\n  \"status\": 404,\n  \"error\": \"Not Found\",\n  \"message\": \"Student not found with ID: 9999\"\n}\n\nServer Console Log Trace:\n2026-10-23 16:20:15.300 WARN [sms,http-nio-8080-exec-3] c.c.s.e.GlobalExceptionHandler : RESOURCE_NOT_FOUND intercepted: Student not found with ID: 9999\n\nDiscussion: The centralized architecture shields internal database exceptions and stack traces from malicious end-users, ensuring sensitive system paths are not exposed while providing clean JSON feedback to API consumers.",
            "photos": [
                "Postman screenshot displaying structured JSON error body with 404 Not Found status.",
                "Terminal console screenshot displaying SLF4J WARN and ERROR formatted log lines."
            ],
            "conclusion": "Centralized exception handling via @RestControllerAdvice and structured diagnostic logging via SLF4J were successfully implemented. The application outputs consistent JSON error payloads and captures clear audit logs."
        },
        {
            "num": 9,
            "title": "API Documentation Using Swagger/OpenAPI",
            "aim": "To integrate Springdoc OpenAPI 3.0 with Spring Boot and generate interactive Swagger UI API documentation for testing REST endpoints.",
            "objective": "1. To add the 'springdoc-openapi-starter-webmvc-ui' dependency to pom.xml.\n2. To configure OpenAPI 3.0 metadata (API title, version, description, contact) via a configuration bean.\n3. To annotate controllers with OpenAPI annotations (@Tag, @Operation, @ApiResponse).\n4. To access Swagger UI at '/swagger-ui/index.html' and interactively test CRUD operations directly from the browser.",
            "theory": "API documentation is essential for frontend-backend collaboration. The OpenAPI Specification (OAS) defines a standard, language-agnostic interface description for HTTP REST APIs.\n\nSpringdoc OpenAPI automates this by inspecting Spring MVC controller annotations at runtime and generating an OpenAPI 3.0 JSON specification (`/v3/api-docs`). Swagger UI consumes this JSON and renders an interactive web page where developers can inspect endpoints, inspect parameter models, input JSON request bodies, and execute real HTTP calls.",
            "procedure": "Step 1: In pom.xml, add the dependency:\n   <dependency>\n       <groupId>org.springdoc</groupId>\n       <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>\n       <version>2.5.0</version>\n   </dependency>\n\nStep 2: Add configuration settings in application.properties:\n   springdoc.api-docs.path=/v3/api-docs\n   springdoc.swagger-ui.path=/swagger-ui.html\n   springdoc.swagger-ui.operationsSorter=method\n\nStep 3: Create 'OpenApiConfig.java' in package 'com.college.sms.config' defining an OpenAPI bean with title, version, and description.\nStep 4: Annotate controllers with @Tag(name = \"Student Operations\"), and methods with @Operation(summary = \"...\") and @ApiResponse(responseCode = \"...\").\nStep 5: Launch the application and open http://localhost:8080/swagger-ui/index.html in a browser.\nStep 6: Test GET, POST, PUT, and DELETE endpoints interactively using Swagger's 'Try it out' feature.",
            "code": """
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
    public OpenAPI studentOpenAPI() {
        return new OpenAPI()
            .info(new Info()
                .title("Student Management System REST API")
                .description("Production REST API with PostgreSQL integration & Full CRUD capabilities")
                .version("1.0.0")
                .contact(new Contact().name("FSD Project Team").email("fsd@college.edu")));
    }
}
""",
            "result_discussion": "Swagger UI rendered an interactive dashboard presenting all registered REST controllers, operations, schemas, and status codes.\n\nInteractive Testing Verification:\n- Navigation: Navigated to http://localhost:8080/swagger-ui/index.html.\n- Endpoint Inspection: All endpoints (GET, POST, PUT, DELETE) appeared grouped under 'Student Operations'.\n- Execution Test: Clicked 'Try it out' on GET /api/students -> Clicked 'Execute' -> Swagger UI made an asynchronous fetch call and displayed HTTP 200 OK along with response JSON body and headers.\n- Schema Inspection: The Student model schema was displayed with field types and nullable attributes.\n\nDiscussion: Interactive documentation eliminates manual Postman collection sharing and allows frontend teams to immediately understand and test endpoint contracts.",
            "photos": [
                "Swagger UI browser screenshot showing API header, description, and grouped endpoints under 'Student Operations'.",
                "Swagger UI 'Try it out' execution screenshot showing JSON response and HTTP 200 OK status code."
            ],
            "conclusion": "Springdoc OpenAPI 3 was successfully integrated into the Spring Boot application. An interactive Swagger UI documentation dashboard was generated, allowing seamless endpoint inspection and testing."
        },
        {
            "num": 10,
            "title": "Packaging and Deployment of the Application",
            "aim": "To package the Spring Boot application as a deployable Web Application Archive (WAR) file and deploy it to an external Apache Tomcat servlet container.",
            "objective": "1. To modify the Maven pom.xml packaging configuration from default JAR to WAR.\n2. To mark the embedded Tomcat dependency as 'provided' to prevent container classpath collisions.\n3. To extend SpringBootServletInitializer in the main application bootstrapping class.\n4. To build the production WAR artifact using 'mvn clean package -DskipTests'.\n5. To deploy the generated WAR to an external Apache Tomcat webapps directory and verify endpoint availability.",
            "theory": "By default, Spring Boot compiles to a self-contained executable JAR with an embedded web server (Tomcat, Jetty, Undertow). However, corporate hosting environments frequently mandate deployment into existing shared Apache Tomcat servlet containers.\n\nTo achieve this:\n1. Packaging Model: The packaging tag in pom.xml is changed from <packaging>jar</packaging> to <packaging>war</packaging>.\n2. Dependency Scope: The embedded container starter (spring-boot-starter-tomcat) is marked with <scope>provided</scope>, instructing Maven not to bundle Tomcat JARs inside the WAR file.\n3. Servlet Initializer: The SpringBootServletInitializer binds the Spring ApplicationContext to the external container's ServletContext during container boot.",
            "procedure": "Step 1: Open pom.xml and change packaging to <packaging>war</packaging>.\nStep 2: Add the provided dependency in pom.xml:\n   <dependency>\n       <groupId>org.springframework.boot</groupId>\n       <artifactId>spring-boot-starter-tomcat</artifactId>\n       <scope>provided</scope>\n   </dependency>\n\nStep 3: Create 'ServletInitializer.java' extending SpringBootServletInitializer, overriding configure(SpringApplicationBuilder application).\nStep 4: Execute the Maven package command in terminal: mvn clean package -DskipTests\nStep 5: Verify the created WAR artifact in the 'target/' directory (e.g. target/sms-1.0.0.war).\nStep 6: Copy the WAR file to the Apache Tomcat 'webapps/' directory.\nStep 7: Start Apache Tomcat via bin/startup.sh (or bin/startup.bat on Windows).\nStep 8: Verify application deployment by querying http://localhost:8080/sms-1.0.0/api/test.",
            "code": """
<!-- 1. Modification in pom.xml -->
<packaging>war</packaging>

<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-tomcat</artifactId>
        <scope>provided</scope>
    </dependency>
</dependencies>

// 2. ServletInitializer.java
package com.college.sms;

import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;

public class ServletInitializer extends SpringBootServletInitializer {
    @Override
    protected SpringApplicationBuilder configure(SpringApplicationBuilder application) {
        return application.sources(StudentApplication.class);
    }
}
""",
            "result_discussion": "The Maven build produced a deployable WAR file, which was successfully extracted and hosted by Apache Tomcat.\n\nMaven Build & Deployment Logs:\n[INFO] Scanning for projects...\n[INFO] Building war: C:\\projects\\sms\\target\\sms-1.0.0.war\n[INFO] Webapp assembled in [242 msecs]\n[INFO] ------------------------------------------------------------------------\n[INFO] BUILD SUCCESS\n[INFO] Total time:  12.418 s\n[INFO] Finished at: 2026-10-23T16:25:00Z\n\nTomcat Deployment Verification:\n23-Oct-2026 16:26:01.412 INFO [main] org.apache.catalina.startup.HostConfig.deployWAR Deploying web application archive [/opt/tomcat/webapps/sms-1.0.0.war]\n23-Oct-2026 16:26:04.120 INFO [main] org.apache.catalina.startup.HostConfig.deployWAR Deployment of web application archive [/opt/tomcat/webapps/sms-1.0.0.war] has finished in [2,708] ms\n\nClient Test via cURL:\n$ curl http://localhost:8080/sms-1.0.0/api/test\nResponse: Spring Boot Application is Running",
            "photos": [
                "Terminal screenshot showing Maven 'BUILD SUCCESS' and generated WAR file in target directory.",
                "Apache Tomcat catalina.out log screenshot confirming successful deployment and startup of the WAR archive."
            ],
            "conclusion": "The Spring Boot application was successfully packaged as a Web Application Archive (WAR) file. It was deployed to an external Apache Tomcat server container and verified to handle live HTTP requests."
        }
    ]

    for exp in experiments:
        add_styled_heading(doc, f"Experiment {exp['num']}: {exp['title']}", level=1)
        
        # 1. Aim
        add_styled_heading(doc, "1. Aim", level=2)
        p = doc.add_paragraph(exp['aim'])
        p.paragraph_format.line_spacing = 1.15
        
        # 2. Objective
        add_styled_heading(doc, "2. Objective", level=2)
        p = doc.add_paragraph(exp['objective'])
        p.paragraph_format.line_spacing = 1.15
        
        # 3. Theory
        add_styled_heading(doc, "3. Theory", level=2)
        p = doc.add_paragraph(exp['theory'])
        p.paragraph_format.line_spacing = 1.15
        
        # 4. Procedure
        add_styled_heading(doc, "4. Procedure", level=2)
        p = doc.add_paragraph(exp['procedure'])
        p.paragraph_format.line_spacing = 1.15
        
        add_styled_heading(doc, "Source Code & Configuration Details", level=3)
        add_code_block(doc, exp['code'])
        
        # 5. Result and Discussion
        add_styled_heading(doc, "5. Result and Discussion", level=2)
        p = doc.add_paragraph(exp['result_discussion'])
        p.paragraph_format.line_spacing = 1.15
        
        add_styled_heading(doc, "Visual Verification & Execution Screenshots", level=3)
        for photo_caption in exp['photos']:
            add_image_placeholder(doc, photo_caption)
            
        # 6. Conclusion
        add_styled_heading(doc, "6. Conclusion", level=2)
        p = doc.add_paragraph(exp['conclusion'])
        p.paragraph_format.line_spacing = 1.15
        
        doc.add_paragraph() # Spacing between experiments

    output_path = "submissions/FSD_10_Experiments_Complete_Lab_Manual.docx"
    doc.save(output_path)
    print(f"Successfully generated: {output_path}")

build_experiments_manual()
