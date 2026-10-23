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
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
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
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = RGBColor(27, 54, 93)
    elif level == 2:
        run.font.name = 'Arial'
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = RGBColor(41, 105, 176)
    elif level == 3:
        run.font.name = 'Arial'
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = RGBColor(51, 51, 51)
    return h

def build_fa2():
    os.makedirs('submissions', exist_ok=True)
    doc = docx.Document()
    
    for sec in doc.sections:
        sec.top_margin = Inches(0.8)
        sec.bottom_margin = Inches(0.8)
        sec.left_margin = Inches(0.8)
        sec.right_margin = Inches(0.8)
        
    # Header block
    header_table = doc.add_table(rows=1, cols=1)
    header_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = header_table.cell(0, 0)
    set_cell_background(c, "1B365D")
    set_cell_margins(c, top=200, bottom=200, left=250, right=250)
    
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("FULL STACK DEVELOPMENT - I (PS-FSD)\nFORMATIVE ASSIGNMENT - 2 (FA-2)\nSEM V | A.Y. 2026-27")
    r.font.name = 'Arial'
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(255, 255, 255)
    
    p2 = c.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = p2.add_run("Comprehensive Technical Solutions & Applied Architecture\nSubject: FSD-1 | Max Marks: 20")
    r2.font.name = 'Arial'
    r2.font.size = Pt(10)
    r2.font.italic = True
    r2.font.color.rgb = RGBColor(200, 220, 245)
    
    doc.add_paragraph()

    # Question Table Summary
    summary_data = [
        ["Q. No.", "Question Overview", "Bloom's Level", "Marks"],
        ["1", "Suitable ORM Technology for Student Management System using Spring Boot & PostgreSQL", "L3 - Apply", "4"],
        ["2", "PostgreSQL Suitability Analysis for E-Commerce Data Consistency & Relations", "L4 - Analyze", "4"],
        ["3", "Spring Boot REST API: @Controller vs @RestController Analysis & JSON Endpoint", "L4 - Analyze, L6 - Create", "4"],
        ["4", "Error Diagnostics & SLF4J Logger Statements for Student Management API", "L4 - Analyze, L6 - Create", "4"],
        ["5", "Interactive API Documentation Tool Selection & Integration (Springdoc / Swagger UI)", "L3 - Apply, L6 - Create", "4"]
    ]
    t = doc.add_table(rows=len(summary_data), cols=4)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(summary_data):
        for c_idx, val in enumerate(row):
            cell = t.cell(r_idx, c_idx)
            set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.name = 'Arial'
            if r_idx == 0:
                set_cell_background(cell, "2969B0")
                run.font.size = Pt(9.5)
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
            else:
                set_cell_background(cell, "F8F9FA" if r_idx % 2 == 1 else "FFFFFF")
                run.font.size = Pt(8.5)
                if c_idx in [0, 3]:
                    run.font.bold = True
    doc.add_paragraph()

    # -------------------------------------------------------------
    # QUESTION 1
    # -------------------------------------------------------------
    add_styled_heading(doc, "Question 1: ORM Technology Selection & Demonstration", level=1)
    q1_text = doc.add_paragraph(
        "Question: A college is developing a Student Management System using Spring Boot and PostgreSQL. "
        "The developer wants to store student objects in the database without writing SQL queries for every operation. "
        "Identify a suitable ORM technology and demonstrate how it simplifies database interactions using an appropriate example. (4 Marks, L3 - Apply)"
    )
    q1_text.paragraph_format.line_spacing = 1.15

    add_styled_heading(doc, "1.1 Identification of Suitable ORM Technology", level=2)
    p = doc.add_paragraph(
        "The most suitable Object-Relational Mapping (ORM) technology for a Spring Boot and PostgreSQL ecosystem is "
        "Spring Data JPA with Hibernate as the underlying JPA provider.\n\n"
        "Why Spring Data JPA + Hibernate is the Industry Standard:\n"
        "1. Abstraction over Boilerplate: Automatically generates SQL queries at runtime for standard CRUD and pagination.\n"
        "2. Transparent Database Portability: Decouples business code from PostgreSQL dialect specifics (sequences, types, syntax).\n"
        "3. First-Class Spring Integration: Integrates seamlessly with Spring's @Transactional boundary management, connection pools (HikariCP), and dependency injection.\n"
        "4. Dirty Checking & First-Level Cache: Updates only modified fields automatically during transaction commit."
    )
    p.paragraph_format.line_spacing = 1.15

    add_styled_heading(doc, "1.2 Practical Demonstration: Raw JDBC vs. Spring Data JPA", level=2)
    p = doc.add_paragraph(
        "In raw JDBC, the developer must manually open a connection, write an explicit SQL string, set parameters on PreparedStatement, "
        "execute the query, handle SQLExceptions, and manually close resources. In contrast, Spring Data JPA eliminates 90% of boilerplate code."
    )
    p.paragraph_format.line_spacing = 1.15

    q1_code = """
// 1. Entity Definition (Domain Model)
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

// 2. Repository Interface (Zero SQL Needed!)
package com.college.sms.repository;

import com.college.sms.entity.Student;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

@Repository
public interface StudentRepository extends JpaRepository<Student, Long> {
    // Built-in methods: save(), findById(), findAll(), deleteById(), count()
    // Dynamic query derivation by method name:
    List<Student> findByDepartmentIgnoreCase(String department);
    Optional<Student> findByEmail(String email);
}

// 3. Service Layer Demonstrating Simplified Persistence
package com.college.sms.service;

import com.college.sms.entity.Student;
import com.college.sms.repository.StudentRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional
public class StudentService {
    private final StudentRepository studentRepository;

    public StudentService(StudentRepository studentRepository) {
        this.studentRepository = studentRepository;
    }

    public Student registerStudent(Student student) {
        // JPA automatically generates: INSERT INTO students (name, email, department) VALUES (?, ?, ?)
        return studentRepository.save(student);
    }

    public Student updateDepartment(Long id, String newDept) {
        // JPA Dirty Checking: entity is updated without writing an explicit UPDATE SQL string!
        Student student = studentRepository.findById(id)
            .orElseThrow(() -> new RuntimeException("Student not found with id: " + id));
        student.setDepartment(newDept);
        return student; // Automatically persisted at transaction commit
    }
}
"""
    add_code_block(doc, q1_code)

    # -------------------------------------------------------------
    # QUESTION 2
    # -------------------------------------------------------------
    add_styled_heading(doc, "Question 2: PostgreSQL Suitability for E-Commerce Applications", level=1)
    q2_text = doc.add_paragraph(
        "Question: An e-commerce application stores customer details, product information, and orders in PostgreSQL. "
        "The application frequently retrieves related records and must maintain data consistency. "
        "Analyze why PostgreSQL is suitable for this application and justify your answer with relevant database features. (4 Marks, L4 - Analyze)"
    )
    q2_text.paragraph_format.line_spacing = 1.15

    add_styled_heading(doc, "2.1 Core Architectural Justification", level=2)
    p = doc.add_paragraph(
        "An e-commerce platform involves high financial stakes: inventory counts must be exact, payment-to-order associations "
        "cannot orphan, and customer checkout cannot suffer dirty reads or race conditions during flash sales. PostgreSQL is "
        "the optimal relational database management system for this workload due to the following specific features:"
    )
    p.paragraph_format.line_spacing = 1.15

    q2_features = [
        ["Database Feature", "Technical Capability", "E-Commerce Impact / Benefit"],
        ["Full ACID Compliance", "Strict Atomicity, Consistency, Isolation, and Durability under write operations.", "Guarantees that when an order is placed, inventory decrement, payment ledger credit, and order record creation succeed together or roll back completely."],
        ["Multi-Version Concurrency Control (MVCC)", "Readers do not block writers, and writers do not block readers.", "High-throughput browsing and catalog filtering do not lock database rows while simultaneous customers complete checkout transactions."],
        ["Declarative Foreign Keys & Cascading Rules", "Referential integrity enforced at database engine level.", "Prevents orphaned orders or line items. Customer deletions can be guarded via RESTRICT or gracefully handled via SET NULL / CASCADE."],
        ["Native JSONB & Semi-Structured Data", "Binary JSON storage with GIN (Generalized Inverted Index) support.", "Allows e-commerce product catalogs to store variable SKU attributes (size, color, material, dimensions) in a single JSONB column without requiring hundreds of sparse columns."],
        ["Advanced Indexing (B-Tree, GIN, Partial)", "Expressive indexing algorithms tailored to varied query access patterns.", "Partial indexes (e.g., CREATE INDEX idx_pending_orders ON orders(id) WHERE status = 'PENDING') accelerate order fulfillment queues by 10x."],
        ["Row-Level Locking (SELECT FOR UPDATE)", "Pessimistic locking semantics for critical transactional windows.", "Prevents overselling during high-volume flash sales by locking the exact inventory row while an order is being confirmed."]
    ]
    t = doc.add_table(rows=len(q2_features), cols=3)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(q2_features):
        for c_idx, val in enumerate(row):
            cell = t.cell(r_idx, c_idx)
            set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
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
                if c_idx == 0:
                    run.font.bold = True
    doc.add_paragraph()

    # -------------------------------------------------------------
    # QUESTION 3
    # -------------------------------------------------------------
    add_styled_heading(doc, "Question 3: @Controller vs @RestController Analysis & JSON API Implementation", level=1)
    q3_text = doc.add_paragraph(
        "Question: A developer needs to build a Spring Boot REST API that returns student details in JSON format when a client sends a GET request. "
        "Analyze the suitability of @Controller and @RestController, select the appropriate annotation, and create a sample controller method to retrieve student details. (4 Marks, L4 - Analyze, L6 - Create)"
    )
    q3_text.paragraph_format.line_spacing = 1.15

    add_styled_heading(doc, "3.1 Comparative Analysis: @Controller vs. @RestController", level=2)
    comp_data = [
        ["Criterion", "@Controller", "@RestController (Recommended)"],
        ["Target Architecture", "Traditional Spring MVC with server-side rendered HTML views (Thymeleaf, JSP).", "RESTful Web Services and Headless APIs returning raw data payloads (JSON / XML)."],
        ["Response Handling", "Return value represents a logical View Name (e.g. \"student-view.html\") resolved by ViewResolver.", "Return value is written directly to HTTP Response Body using HttpMessageConverter (Jackson)."],
        ["Need for @ResponseBody", "Mandatory on every method if JSON response is desired; otherwise Spring expects a template view.", "Built-in! @RestController is a convenience meta-annotation combining @Controller + @ResponseBody."],
        ["Developer Velocity & Cleanliness", "Error-prone and verbose for API-first backends due to repetitive @ResponseBody annotations.", "Clean, concise, and standard for modern single-page apps (React, Next.js, mobile clients)."]
    ]
    t = doc.add_table(rows=len(comp_data), cols=3)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(comp_data):
        for c_idx, val in enumerate(row):
            cell = t.cell(r_idx, c_idx)
            set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
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
                if c_idx in [0, 2]:
                    run.font.bold = True
    doc.add_paragraph()

    add_styled_heading(doc, "3.2 Selection & Sample REST Controller Implementation", level=2)
    p = doc.add_paragraph(
        "Selection: `@RestController` is the clear choice. It configures Jackson's ObjectMapper to serialize Java objects "
        "directly into JSON representations with appropriate `application/json` Content-Type headers."
    )
    p.paragraph_format.line_spacing = 1.15

    q3_code = """
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
@CrossOrigin(origins = "*") // Allows Next.js / frontend client consumption
public class StudentController {

    private final StudentRepository studentRepository;

    public StudentController(StudentRepository studentRepository) {
        this.studentRepository = studentRepository;
    }

    /**
     * Retrieves student details by ID and returns them formatted as JSON.
     * HTTP Method: GET
     * URL Endpoint: /api/students/{id}
     */
    @GetMapping(value = "/{id}", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Student> getStudentById(@PathVariable Long id) {
        Student student = studentRepository.findById(id)
            .orElseThrow(() -> new ResponseStatusException(
                HttpStatus.NOT_FOUND, 
                "Student record not found for ID: " + id
            ));
        
        return ResponseEntity.ok(student);
    }
}
"""
    add_code_block(doc, q3_code)

    # -------------------------------------------------------------
    # QUESTION 4
    # -------------------------------------------------------------
    add_styled_heading(doc, "Question 4: Diagnostic Logging Strategy & SLF4J Implementation", level=1)
    q4_text = doc.add_paragraph(
        "Question: A Student Management API occasionally fails while retrieving student records. "
        "The development team needs meaningful logs to identify failed operations and troubleshoot errors. "
        "Analyze the information that should be recorded and write suitable SLF4J Logger statements to log the student ID, operation, and exception details. (4 Marks, L4 - Analyze, L6 - Create)"
    )
    q4_text.paragraph_format.line_spacing = 1.15

    add_styled_heading(doc, "4.1 Information Architecture for Production Diagnostics", level=2)
    p = doc.add_paragraph(
        "When an API operation fails, production logs must provide sufficient context to reproduce and remediate the issue without "
        "violating data privacy regulations. The required diagnostic fields are:\n"
        "1. Operation Name & HTTP Verb: e.g., 'FETCH_STUDENT_BY_ID' or 'UPDATE_STUDENT'.\n"
        "2. Entity Identifier: The targeted student ID (e.g., studentId=1042).\n"
        "3. Timestamp & Correlation / Trace ID: Correlates distributed requests across services.\n"
        "4. Client Context: Client IP, user agent, or authenticated principal.\n"
        "5. Exception Details & Root Cause: The exact exception class, localized error message, and full stack trace (logged at ERROR level).\n"
        "6. PII Masking: Passwords, sensitive personal identifiers, or auth tokens must never be logged."
    )
    p.paragraph_format.line_spacing = 1.15

    add_styled_heading(doc, "4.2 Production SLF4J Implementation with Exception Handling", level=2)
    q4_code = """
package com.college.sms.service;

import com.college.sms.entity.Student;
import com.college.sms.exception.ResourceNotFoundException;
import com.college.sms.repository.StudentRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

@Service
public class StudentRetrievalService {

    // SLF4J Logger initialization (Logger abstraction supported by Logback runtime)
    private static final Logger log = LoggerFactory.getLogger(StudentRetrievalService.class);

    private final StudentRepository studentRepository;

    public StudentRetrievalService(StudentRepository studentRepository) {
        this.studentRepository = studentRepository;
    }

    public Student getStudent(Long studentId) {
        final String operation = "FETCH_STUDENT_BY_ID";

        // 1. Entry / Trace logging at DEBUG / INFO level with parameterized logging (avoids string concatenation overhead)
        log.info("Starting operation [{}] for studentId: {}", operation, studentId);

        try {
            return studentRepository.findById(studentId)
                .orElseThrow(() -> {
                    // 2. Warning level log for anticipated business domain conditions (e.g. ID not found)
                    log.warn("Operation [{}] failed: Student record not found for studentId: {}", operation, studentId);
                    return new ResourceNotFoundException("Student not found with ID: " + studentId);
                });

        } catch (ResourceNotFoundException ex) {
            // Re-throw for ControllerAdvice to translate into HTTP 404
            throw ex;

        } catch (Exception ex) {
            // 3. Error level log capturing unexpected runtime anomalies (e.g., DB connection dropped, SQL timeout)
            // Notice: The last parameter is the Throwable 'ex' which logs the complete stack trace automatically!
            log.error("Operation [{}] encountered severe unexpected failure for studentId: {}. Error message: {}", 
                      operation, studentId, ex.getMessage(), ex);
            
            throw new RuntimeException("Database retrieval error for student ID " + studentId, ex);
        }
    }
}
"""
    add_code_block(doc, q4_code)

    # -------------------------------------------------------------
    # QUESTION 5
    # -------------------------------------------------------------
    add_styled_heading(doc, "Question 5: Interactive API Documentation (Springdoc OpenAPI / Swagger UI)", level=1)
    q5_text = doc.add_paragraph(
        "Question: A development team has implemented REST APIs for adding, retrieving, updating, and deleting student records. "
        "The testing team needs interactive API documentation to inspect endpoints, provide request parameters, and test responses. "
        "Select a suitable documentation tool and design the steps required to integrate it with Spring Boot and test the APIs. (4 Marks, L3 - Apply, L6 - Create)"
    )
    q5_text.paragraph_format.line_spacing = 1.15

    add_styled_heading(doc, "5.1 Tool Selection: Springdoc OpenAPI 3 with Swagger UI", level=2)
    p = doc.add_paragraph(
        "The standard and most capable tool for Spring Boot is Springdoc OpenAPI (`springdoc-openapi-starter-webmvc-ui`). "
        "Unlike deprecated legacy libraries (Springfox), Springdoc natively supports Spring Boot 3.x, OpenAPI 3.0 specification, "
        "Jakarta EE annotations, and generates a rich, responsive interactive testing sandbox at `/swagger-ui/index.html`."
    )
    p.paragraph_format.line_spacing = 1.15

    add_styled_heading(doc, "5.2 Step-by-Step Integration Design", level=2)
    p = doc.add_paragraph(
        "Step 1: Add the Springdoc Starter Dependency to pom.xml\n"
        "Step 2: Configure OpenAPI metadata in application.properties or Java Config\n"
        "Step 3: Enrich REST Controllers and DTOs with OpenAPI annotations (@Tag, @Operation, @ApiResponse)\n"
        "Step 4: Launch the application and test CRUD operations interactively via Swagger UI"
    )
    p.paragraph_format.line_spacing = 1.15

    q5_code = """
<!-- STEP 1: Add dependency to pom.xml -->
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.5.0</version>
</dependency>

# STEP 2: Configure in application.properties
springdoc.api-docs.path=/v3/api-docs
springdoc.swagger-ui.path=/swagger-ui.html
springdoc.swagger-ui.operationsSorter=method
springdoc.swagger-ui.tagsSorter=alpha

// STEP 3: Enriched Controller with OpenAPI Annotations
package com.college.sms.controller;

import com.college.sms.entity.Student;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/students")
@Tag(name = "Student Management", description = "Endpoints for creating, reading, updating, and deleting student records")
public class StudentOpenApiController {

    @Operation(summary = "Create a new student", description = "Persists a new student record in PostgreSQL database")
    @ApiResponses({
        @ApiResponse(responseCode = "201", description = "Student successfully created"),
        @ApiResponse(responseCode = "400", description = "Invalid payload or duplicate email")
    })
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public ResponseEntity<Student> createStudent(@RequestBody Student student) {
        // Implementation
        return new ResponseEntity<>(student, HttpStatus.CREATED);
    }

    @Operation(summary = "Get student by ID", description = "Fetches complete student profile using unique database ID")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Student details found and returned in JSON"),
        @ApiResponse(responseCode = "404", description = "Student with given ID does not exist")
    })
    @GetMapping("/{id}")
    public ResponseEntity<Student> getStudentById(
        @Parameter(description = "Primary key ID of the student", example = "1")
        @PathVariable Long id) {
        // Implementation
        return ResponseEntity.ok(new Student());
    }
}
"""
    add_code_block(doc, q5_code)

    add_styled_heading(doc, "5.3 Testing Workflow in Swagger UI", level=2)
    p = doc.add_paragraph(
        "1. Open Browser: Navigate to http://localhost:8080/swagger-ui/index.html\n"
        "2. Inspect Endpoints: Review all grouped endpoints under 'Student Management' (GET, POST, PUT, DELETE).\n"
        "3. Interactive Execution ('Try it out'):\n"
        "   - Select POST /api/students -> Click 'Try it out' -> Paste JSON body -> Click 'Execute'.\n"
        "   - Inspect Server Response: Verify HTTP 201 Created and returned JSON containing generated ID.\n"
        "   - Select GET /api/students/{id} -> Enter ID -> Click 'Execute' -> Verify HTTP 200 OK and response body."
    )
    p.paragraph_format.line_spacing = 1.15

    output_path = "submissions/FA2_FSD_Formative_Assignment_2_Submission.docx"
    doc.save(output_path)
    print(f"Successfully generated: {output_path}")

build_fa2()
