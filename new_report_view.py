class GenerateStudentReportView(APIView):
    """
    Generate a comprehensive student report based on actual performance data from frontend.
    
    This view accepts:
    - Student performance data (marks, sections, questions)
    - Test session information
    - Optional proctoring data
    
    Returns:
    - Comprehensive report with calculations
    - Performance analytics
    - Optional AI analysis (if Gemini API key is set)
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Validate input data
        serializer = GenerateStudentReportSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'error': 'Invalid data provided',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        
        try:
            # Get assessment
            assessment = Assessment.objects.select_related().get(id=data['assessment_id'])
            
            # Get student or user
            student = None
            candidate = None
            
            if data.get('student_email'):
                student = Student.objects.get(email=data['student_email'])
                participant_type = 'student'
            else:
                candidate = User.objects.get(email=data['candidate_email'])
                participant_type = 'user'
            
            # Calculate report metrics
            report_data = self._calculate_report_metrics(data, assessment)
            
            # Create report record
            report = self._create_report_record(
                assessment, student, candidate, data, report_data
            )
            
            # Generate comprehensive response
            response_data = self._generate_response(
                report, assessment, student, candidate, report_data, data
            )
            
            return Response({
                'message': 'Student report generated successfully',
                'report_id': report.id,
                'participant_type': participant_type,
                **response_data
            }, status=status.HTTP_201_CREATED)
            
        except Assessment.DoesNotExist:
            return Response({
                'error': 'Assessment not found',
                'assessment_id': data['assessment_id']
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Student.DoesNotExist:
            return Response({
                'error': 'Student not found',
                'email': data.get('student_email')
            }, status=status.HTTP_404_NOT_FOUND)
            
        except User.DoesNotExist:
            return Response({
                'error': 'User not found',
                'email': data.get('candidate_email')
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({
                'error': 'Failed to generate report',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _calculate_report_metrics(self, data, assessment):
        """Calculate comprehensive report metrics from performance data"""
        
        # Initialize totals
        total_marks_obtained = 0
        total_questions = 0
        total_attempted = 0
        total_correct = 0
        total_wrong = 0
        total_time_spent = 0
        
        # Section-wise analysis
        sections_analysis = {}
        question_type_analysis = {'coding': {}, 'non-coding': {}}
        topic_analysis = {}
        detailed_questions = []
        
        for section_data in data['sections']:
            section_id = section_data['section_id']
            section = Section.objects.get(id=section_id)
            
            # Section metrics
            section_metrics = {
                'section_id': section_id,
                'section_name': section.name,
                'total_questions': len(section_data['questions']),
                'attempted': 0,
                'correct': 0,
                'wrong': 0,
                'marks_obtained': 0,
                'total_marks': 0,
                'time_spent': section_data.get('time_spent', 0),
                'accuracy': 0
            }
            
            # Process each question in the section
            for q_data in section_data['questions']:
                try:
                    question = Question.objects.get(id=q_data['question_id'])
                    
                    # Question details
                    question_detail = {
                        'question_id': question.id,
                        'question_text': question.question_text[:100] + '...' if len(question.question_text) > 100 else question.question_text,
                        'question_type': question.question_type,
                        'section_name': section.name,
                        'topic': getattr(question, 'topic', 'General'),
                        'difficulty': getattr(question, 'difficulty', 'Medium'),
                        'marks': question.marks,
                        'negative_marks': question.negative_marks,
                        'is_attempted': q_data['is_attempted'],
                        'is_correct': q_data['is_correct'],
                        'marks_obtained': q_data['marks_obtained'],
                        'time_spent': q_data.get('time_spent', 0)
                    }
                    
                    # Add answer details
                    if question.question_type == 'non-coding' and q_data.get('selected_option_index') is not None:
                        question_detail['selected_option'] = q_data['selected_option_index']
                        if hasattr(question, 'correct_option_index'):
                            question_detail['correct_option'] = question.correct_option_index
                    elif question.question_type == 'coding' and q_data.get('code_answer'):
                        question_detail['code_submitted'] = bool(q_data['code_answer'].strip())
                    
                    detailed_questions.append(question_detail)
                    
                    # Update section metrics
                    section_metrics['total_marks'] += question.marks
                    section_metrics['marks_obtained'] += q_data['marks_obtained']
                    
                    if q_data['is_attempted']:
                        section_metrics['attempted'] += 1
                        total_attempted += 1
                        
                        if q_data['is_correct']:
                            section_metrics['correct'] += 1
                            total_correct += 1
                        else:
                            section_metrics['wrong'] += 1
                            total_wrong += 1
                    
                    # Update question type analysis
                    q_type = question.question_type
                    if q_type not in question_type_analysis:
                        question_type_analysis[q_type] = {'attempted': 0, 'correct': 0, 'wrong': 0, 'marks_obtained': 0}
                    
                    if q_data['is_attempted']:
                        question_type_analysis[q_type]['attempted'] += 1
                        question_type_analysis[q_type]['marks_obtained'] += q_data['marks_obtained']
                        
                        if q_data['is_correct']:
                            question_type_analysis[q_type]['correct'] += 1
                        else:
                            question_type_analysis[q_type]['wrong'] += 1
                    
                    # Update topic analysis
                    topic = getattr(question, 'topic', 'General')
                    if topic not in topic_analysis:
                        topic_analysis[topic] = {'attempted': 0, 'correct': 0, 'wrong': 0, 'marks_obtained': 0}
                    
                    if q_data['is_attempted']:
                        topic_analysis[topic]['attempted'] += 1
                        topic_analysis[topic]['marks_obtained'] += q_data['marks_obtained']
                        
                        if q_data['is_correct']:
                            topic_analysis[topic]['correct'] += 1
                        else:
                            topic_analysis[topic]['wrong'] += 1
                    
                    # Update totals
                    total_questions += 1
                    total_marks_obtained += q_data['marks_obtained']
                    total_time_spent += q_data.get('time_spent', 0)
                    
                except Question.DoesNotExist:
                    continue  # Skip invalid question IDs
            
            # Calculate section accuracy
            if section_metrics['attempted'] > 0:
                section_metrics['accuracy'] = (section_metrics['correct'] / section_metrics['attempted']) * 100
            
            sections_analysis[section_id] = section_metrics
        
        # Get total possible marks from assessment
        total_possible_marks = sum(
            Question.objects.filter(assessment=assessment).values_list('marks', flat=True)
        )
        
        # Calculate overall metrics
        overall_percentage = (total_marks_obtained / total_possible_marks * 100) if total_possible_marks > 0 else 0
        overall_accuracy = (total_correct / total_attempted * 100) if total_attempted > 0 else 0
        
        return {
            'total_marks_obtained': total_marks_obtained,
            'total_possible_marks': total_possible_marks,
            'percentage': round(overall_percentage, 2),
            'accuracy': round(overall_accuracy, 2),
            'total_questions': total_questions,
            'total_attempted': total_attempted,
            'total_correct': total_correct,
            'total_wrong': total_wrong,
            'questions_left': total_questions - total_attempted,
            'total_time_spent': total_time_spent,
            'sections_analysis': list(sections_analysis.values()),
            'question_type_analysis': question_type_analysis,
            'topic_analysis': topic_analysis,
            'detailed_questions': detailed_questions
        }

    def _create_report_record(self, assessment, student, candidate, data, report_data):
        """Create and save report record to database"""
        import uuid
        
        report = Report.objects.create(
            id=str(uuid.uuid4()),
            assessment=assessment,
            student=student,
            candidate=candidate,
            started_at=data['started_at'],
            ended_at=data['ended_at'],
            submitted_at=data['submitted_at'],
            status='completed',
            total_marks=report_data['total_possible_marks'],
            obtained_marks=report_data['total_marks_obtained'],
            percentage=report_data['percentage'],
            percentile=0,  # Calculate later if needed
            window_switch_count=data.get('window_switch_count', 0),
            is_cheating=data.get('is_cheating', False),
            cheating_reason=data.get('cheating_reason', '')
        )
        
        return report

    def _generate_response(self, report, assessment, student, candidate, report_data, original_data):
        """Generate comprehensive response with all analytics"""
        
        # Participant info
        if student:
            participant_info = {
                'id': student.id,
                'email': student.email,
                'name': student.full_name,
                'type': 'student'
            }
        else:
            participant_info = {
                'id': candidate.id,
                'email': candidate.email,
                'name': getattr(candidate, 'full_name', candidate.email),
                'type': 'user'
            }
        
        # Time analysis
        time_analysis = {
            'total_time_spent': report_data['total_time_spent'],
            'average_time_per_question': (
                report_data['total_time_spent'] / report_data['total_attempted'] 
                if report_data['total_attempted'] > 0 else 0
            ),
            'started_at': original_data['started_at'].isoformat(),
            'ended_at': original_data['ended_at'].isoformat(),
            'submitted_at': original_data['submitted_at'].isoformat(),
            'total_duration': int((original_data['ended_at'] - original_data['started_at']).total_seconds())
        }
        
        # Performance insights
        insights = self._generate_insights(report_data)
        
        response = {
            'summary': {
                'report_id': report.id,
                'participant': participant_info,
                'assessment': {
                    'id': assessment.id,
                    'title': assessment.title,
                    'type': assessment.assessment_type,
                    'total_marks': report_data['total_possible_marks']
                },
                'overall_performance': {
                    'marks_obtained': report_data['total_marks_obtained'],
                    'total_marks': report_data['total_possible_marks'],
                    'percentage': report_data['percentage'],
                    'accuracy': report_data['accuracy'],
                    'questions_attempted': report_data['total_attempted'],
                    'questions_correct': report_data['total_correct'],
                    'questions_wrong': report_data['total_wrong'],
                    'questions_left': report_data['questions_left']
                },
                'time_analysis': time_analysis,
                'sections_performance': report_data['sections_analysis'],
                'question_types_performance': report_data['question_type_analysis'],
                'topics_performance': report_data['topic_analysis'],
                'insights': insights
            },
            'detailed_questions': report_data['detailed_questions']
        }
        
        # Add AI analysis if available
        ai_analysis = self._get_ai_analysis(report_data)
        if ai_analysis:
            response['ai_analysis'] = ai_analysis
        
        return response

    def _generate_insights(self, report_data):
        """Generate performance insights"""
        insights = []
        
        # Overall performance insights
        if report_data['percentage'] >= 80:
            insights.append("Excellent overall performance!")
        elif report_data['percentage'] >= 60:
            insights.append("Good performance with room for improvement")
        else:
            insights.append("Needs significant improvement")
        
        # Accuracy insights
        if report_data['accuracy'] >= 90:
            insights.append("Very high accuracy - great attention to detail")
        elif report_data['accuracy'] < 50:
            insights.append("Low accuracy - consider reviewing fundamentals")
        
        # Section-wise insights
        best_section = max(report_data['sections_analysis'], key=lambda x: x.get('accuracy', 0))
        worst_section = min(report_data['sections_analysis'], key=lambda x: x.get('accuracy', 0))
        
        insights.append(f"Strongest area: {best_section['section_name']}")
        insights.append(f"Needs improvement: {worst_section['section_name']}")
        
        # Question type insights
        for q_type, stats in report_data['question_type_analysis'].items():
            if stats.get('attempted', 0) > 0:
                type_accuracy = (stats['correct'] / stats['attempted']) * 100
                if type_accuracy < 50:
                    insights.append(f"Focus on {q_type} questions")
        
        return insights

    def _get_ai_analysis(self, report_data):
        """Generate AI analysis if Gemini API key is available"""
        try:
            import os
            api_key = os.environ.get('GEMINI_API_KEY')
            if not api_key:
                return {"info": "Set GEMINI_API_KEY environment variable to enable AI analysis"}
            
            import google.generativeai as genai
            import json
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Create analysis prompt
            prompt = f"""
            Analyze this student's assessment performance and provide detailed insights:
            
            Overall Performance:
            - Score: {report_data['total_marks_obtained']}/{report_data['total_possible_marks']} ({report_data['percentage']}%)
            - Accuracy: {report_data['accuracy']}%
            - Questions: {report_data['total_attempted']} attempted, {report_data['total_correct']} correct
            
            Section Performance: {json.dumps(report_data['sections_analysis'])}
            Topic Performance: {json.dumps(report_data['topic_analysis'])}
            
            Provide a JSON response with:
            1. "strengths": Array of strongest areas
            2. "weaknesses": Array of areas needing improvement  
            3. "recommendations": Array of specific study suggestions
            4. "next_steps": Array of actionable next steps
            5. "overall_assessment": Brief overall evaluation
            
            Focus on constructive, actionable advice.
            """
            
            response = model.generate_content(prompt)
            
            # Parse AI response
            if hasattr(response, 'text'):
                ai_text = response.text
                # Try to extract JSON from response
                try:
                    import re
                    json_match = re.search(r'\{.*\}', ai_text, re.DOTALL)
                    if json_match:
                        return json.loads(json_match.group())
                    else:
                        return {"raw_analysis": ai_text}
                except:
                    return {"raw_analysis": ai_text}
            
        except Exception as e:
            return {"error": f"AI analysis failed: {str(e)}"}
        
        return None
